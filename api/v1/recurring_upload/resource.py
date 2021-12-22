from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from api.v1.user_role_permission_info.model import permission_required
from api.v1.upload_file.model import UploadFileModel
import config
import sys
import os
import uuid

from system_core.csvconversion.csvconversion import (get_headers, get_content, csv_list_to_dicts)
from api.v1.client.model import ClientModel
from system_core.helper.array_to_dict import array_to_dict_by_key_lower, array_to_dict_by_keys_lower
from system_core.helper.populate_field import populate_field, populate_field_dict
from api.v1.employee.model import EmployeeModel
from api.v1.pay_element.model import PayElementModel
from api.v1.schedule.model import ScheduleModel
from api.v1.recurring_element.model import RecurringElementModel
from system_core.csvconversion.post_audit_logs import post_masterfile_audit_logs
from system_core.recurring_element.post_recurring_elements import insert_update_recurring_element_entries
from system_core.helper.convert_date import convert_date



GET_RECURRING_UPLOAD = 'get_recurring_upload'
POST_RECURRING_UPLOAD = 'post_recurring_upload'

ALLOWED_EXTENSIONS = set(['csv'])
UPLOAD_FOLDER = config.UPLOAD_DIR
UPDATE_HEADERS = [
    'week_no',
    'amount',
    'is_active',
    'start_date',
    'end_date',
    'remarks'
]
DATE_FIELDS = [
    'start_date',
    'end_date'
]


parser = reqparse.RequestParser()
parser.add_argument('file', type=FileStorage, location='files')


class RecurringUpload(Resource):
    @jwt_required
    @permission_required(GET_RECURRING_UPLOAD)
    def get(self):
        return {"message": "GET"}, 200
    
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()

        files = request.files.getlist('file')
        client_id = request.form.get('compid')

        client = ClientModel.query.get(client_id)
        if client:
            client_db = client.db_name
        else:
            return {
                'success': False, 
                'errors': [[0, '-', '-', '-', 'Client not found']],
                'message': 'File uploading failed.',
                'row_count': 0,
                'skips': [],
                'audit_logs': []
            }, 200

        success = True
        errors = []
        skips = []
        audit_logs = []
        updated_rows = 0
        
        for file in files:
            if file and allowed_file(file.filename):
                file_uid = uuid.uuid1().hex
                filename = secure_filename(file.filename)
                fullpath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(fullpath)

                upload_file = UploadFileModel(file_uid=file_uid, fullpath=fullpath, filename=filename)
                upload_file.save_to_db()

                headers, duplicate_headers = get_headers(fullpath)
                
                if len(duplicate_headers) > 0:
                    errors.append([0, '-', '-', '-', 'File has duplicate headers: ' + ', '.join(duplicate_headers)])
                    continue
                
                content = get_content(fullpath)

                """Insert code here to convert header to raw_code"""
                for i in range(len(headers)):
                    headers[i] = headers[i].lower().replace(" ", "_")

                # Check required fields
                if 'employee_number' not in headers or 'code' not in headers:
                    errors.append([0, '-', '-', '-', 'EMPLOYEE_NUMBER or CODE field is not present in the upload file'])
                    continue

                data = {}
                data['client_db'] = client_db

                csv_data = csv_list_to_dicts(headers, content)

                employees = array_to_dict_by_key_lower(EmployeeModel.get_all_employees(client_db), 'employee_number')
                pay_elements = array_to_dict_by_key_lower(PayElementModel.get_all(client_db), 'code')
                schedules = array_to_dict_by_key_lower(ScheduleModel.get_all(client_db), "code")
                recurring_elements = array_to_dict_by_keys_lower(populate_field(schedules, populate_field(pay_elements, populate_field(employees, RecurringElementModel.get_all(client_db), 'id', 'employee_id', 'employee_number'), 'id', 'pay_element_id', 'code', 'pay_element_code'), 'id', 'schedule_id', 'code', 'schedule_code'), ['employee_number', 'pay_element_code'])
                audit_logs = []
                row_num = 1

                for row in csv_data:
                    row_num += 1
                    has_update = False

                    if row['employee_number'].lower() not in employees:
                        errors.append([row_num, row['employee_number'], 'employee_number', row['employee_number'], "employee number not found in employees"])
                        skips.append([row_num, row['employee_number'], row['code']])
                        continue

                    if row['code'].lower() not in pay_elements:
                        errors.append([row_num, row['employee_number'], 'code', row['code'], "code not found in pay_elements"])
                        skips.append([row_num, row['employee_number'], row['code']])
                        continue

                    employee = employees[row['employee_number'].lower()]
                    middle_initial = "" if not employee['middlename'] else employee['middlename'][0]
                    name = employee['lastname'] + ', ' + employee['firstname'] + ' ' + middle_initial if not employee['suffix'] else employee['lastname'] + ' ' + employee['suffix'] + ', ' + employee['firstname'] + ' ' + middle_initial
                    if 'name' in row:
                        if row['name'].upper() != name.upper() and row['name'].upper() != (name.upper() + "."):
                            errors.append([row_num, row['employee_number'], 'name', row['name'], "name is not the same in employee record"])

                    lookup_value = row['employee_number'].lower() + row['code'].lower()

                    transaction_type = "Add"
                    record = {}
                    if lookup_value in recurring_elements:
                        record = recurring_elements[lookup_value]
                        transaction_type = "Edit"
                    else:
                        # Check SCHEDULE_CODE
                        if 'week_no' not in row:
                            errors.append([row_num, row['employee_number'], 'week_no', '', "week_no required for a new recurring element"])
                            continue

                        if row['week_no'].lower() not in schedules:
                            errors.append([row_num, row['employee_number'], 'week_no', row['week_no'], "week_no not found in schedules"])
                            continue

                        # Check AMOUNT
                        if 'amount' not in row:
                            errors.append([row_num, row['employee_number'], 'amount', '', "amount required for a new recurring element"])
                            continue

                        # If new record, initialize record
                        record['employee_id'] = employees[row['employee_number'].lower()]['id']
                        record['employee_number'] = row['employee_number']
                        record['pay_element_id'] = pay_elements[row['code'].lower()]['id']
                        record['pay_element_code'] = row['code']

                    for field in UPDATE_HEADERS:
                        # Check if field in row
                        if field not in row:
                            continue

                        t_code = field
                        tcvalue = row[field]
                        old_value = ""

                        # Fields with reference tables
                        # SCHEDULE_CODE
                        if field == 'week_no':
                            t_code = "schedule_id"
                            if tcvalue.lower() not in schedules:
                                errors.append([row_num, row['employee_number'], field, tcvalue, "week_no not found in schedules"])
                                continue
                            tcvalue = schedules[tcvalue.lower()]['id']

                        if field == 'start_date' or field == 'end_date':
                            if tcvalue == '':
                                tcvalue = None

                        # Validate dates
                        if field in DATE_FIELDS:
                            if tcvalue:
                                tcvalue = convert_date(tcvalue)
                                if tcvalue is None:
                                    errors.append([row_num, row['employee_number'], field, row[field], "invalid date"])
                                    continue

                        if transaction_type == "Edit":
                            old_value = record[t_code]

                        if t_code in record:
                            try:
                                if type(record[t_code]) is str:
                                    tcvalue = str(tcvalue)
                                if type(record[t_code]) is int:
                                    tcvalue = int(tcvalue)
                                if type(record[t_code]) is float:
                                    tcvalue = float(tcvalue)
                                if type(record[t_code]) is bool:
                                    tcvalue = bool(int(tcvalue))

                                if record[t_code] == tcvalue:
                                    continue
                            except Exception as e:
                                errors.append([row_num, row['employee_number'], field, row[field], str(e)])
                                continue

                        # Insert code here to update column with value
                        record[t_code] = tcvalue
                        has_update = True

                        recurring_elements[lookup_value] = record

                        # Insert code here to input audit log
                        audit_log = {
                            'employee_number': row['employee_number'],
                            'tablename':  'recurring_elements',
                            'field': t_code,
                            'code': row['code'],
                            'old_value': old_value if type(old_value) is str else str(old_value),
                            'new_value': tcvalue if type(tcvalue) is str else str(tcvalue),
                            'transaction_type': transaction_type,
                            'username': current_user
                        }
                        audit_logs.append(audit_log)
                    
                    if has_update:
                        updated_rows += 1
                    else:
                        skips.append([row_num, row['employee_number'], row['code']])

                data['headers'] = headers
                data['content'] = content
                data['csv_data'] = csv_data
                data['employees'] = employees
                data['audit_logs'] = audit_logs
                data['recurring_elements'] = recurring_elements

                post_masterfile_audit_logs(data)
                
                # Populate employee_id, pay_element_id, schedule_id
                data['recurring_elements'] = array_to_dict_by_keys_lower(populate_field_dict(schedules, data['recurring_elements'], 'id', 'schedule_id', 'code', 'schedule_code'), ['employee_number', 'pay_element_code'])
                insert_update_recurring_element_entries(data)
            else:
                errors.append([0, '-', '-', '-', 'File type is not allowed'])
                continue
        
        if success:
            message = 'File uploaded successfully.' if len(errors)==0 else 'File uploaded successfully but with errors.'
            message = message if updated_rows>0 else 'No records updated.'
            return {
                'success': success, 
                'errors': errors,
                'message': message,
                'row_count': updated_rows,
                'skips': skips,
                'audit_logs': audit_logs
            }, 201
        
        else:
            return {
                'success': success, 
                'errors': errors,
                'message': 'No records updated.',
                'row_count': updated_rows,
                'skips': skips,
                'audit_logs': audit_logs
            }, 200

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
