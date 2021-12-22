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
import datetime
import re

from system_core.csvconversion.csvconversion import (get_headers, get_content, csv_list_to_dicts)
from api.v1.client.model import ClientModel
from system_core.helper.array_to_dict import array_to_dict_by_key_lower, array_to_dict_by_keys_lower
from system_core.helper.populate_field import populate_field, populate_field_dict
from api.v1.employee.model import EmployeeModel
from api.v1.pay_element.model import PayElementModel
from api.v1.schedule.model import ScheduleModel
from api.v1.loan_code_info.model import LoanCodeInfoModel
from api.v1.loan.model import LoanModel
from api.v1.employment_status.model import EmploymentStatusModel
from system_core.csvconversion.post_audit_logs import post_masterfile_audit_logs
from system_core.loan.post_loans import insert_update_loan_entries
from system_core.loan.post_loan_payments import post_entry as post_loan_payment_entry
from system_core.helper.convert_date import convert_date



GET_LOAN_UPLOAD = 'get_loan_upload'
POST_LOAN_UPLOAD = 'post_loan_upload'

ALLOWED_EXTENSIONS = set(['csv'])
UPLOAD_FOLDER = config.UPLOAD_DIR
UPDATE_HEADERS = [
    'ded_dur',
    'first_deduction',
    'loan_amount',
    'principal_amount',
    'outstanding_balance',
    'installment_amount',
    'is_suspended',
    'is_stopped',
    'no_of_installment',
    'remarks',
    'last_installment_no'
]
REQ_HEADERS = [
    'name',
    'ded_dur',
    'first_deduction',
    'loan_amount',
    'principal_amount',
    'outstanding_balance',
    'installment_amount',
    'no_of_installment'
]
DATE_FIELDS = [
    'loan_date',
    'first_deduction'
]


parser = reqparse.RequestParser()
parser.add_argument('file', type=FileStorage, location='files')


class LoanUpload(Resource):
    @jwt_required
    @permission_required(GET_LOAN_UPLOAD)
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
                'zero_outs': [],
                'audit_logs': []
            }, 200

        success = True
        errors = []
        skips = []
        zero_outs = []
        audit_logs = []
        updated_rows = 0

        deduction_date = "2021-01-01"
        is_hidden = False
        
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
                if 'employee_number' not in headers or 'loan_code' not in headers or 'loan_date' not in headers:
                    errors.append([0, '-', '-', '-', 'EMPLOYEE_NUMBER or LOAN_CODE or LOAN_DATE field is not present in the upload file'])
                    continue

                data = {}
                data['client_db'] = client_db

                csv_data = csv_list_to_dicts(headers, content)

                employees = array_to_dict_by_key_lower(EmployeeModel.get_all_employees(client_db), 'employee_number')
                loan_codes = array_to_dict_by_key_lower(LoanCodeInfoModel.get_all(client_db), 'pay_element_code')
                schedules = array_to_dict_by_key_lower(ScheduleModel.get_all(client_db), "code")
                loans = array_to_dict_by_keys_lower(populate_field(schedules, populate_field(loan_codes, populate_field(employees, LoanModel.get_all(client_db), 'id', 'employee_id', 'employee_number'), 'id', 'loan_code_id', 'pay_element_code', 'loan_code'), 'id', 'schedule_id', 'code', 'schedule_code'), ['employee_number', 'loan_code', 'loan_date'])
                employment_status = array_to_dict_by_key_lower(EmploymentStatusModel.get_all(client_db), 'id')
                audit_logs = []
                row_num = 1

                for row in csv_data:
                    row_num += 1
                    has_update = False

                    if row['employee_number'].lower() not in employees:
                        errors.append([row_num, row['employee_number'], 'employee_number', row['employee_number'], "employee number not found in employees"])
                        skips.append([row_num, row['employee_number'], row['loan_code'], row['loan_date']])
                        continue

                    if row['loan_code'].lower() not in loan_codes:
                        errors.append([row_num, row['employee_number'], 'loan_code', row['loan_code'], "loan_code not found in loan_codes"])
                        skips.append([row_num, row['employee_number'], row['loan_code'], row['loan_date']])
                        continue

                    row['loan_date'] = convert_date(row['loan_date'])
                    if row['loan_date'] is None or row['loan_date'] == "":
                        errors.append([row_num, row['employee_number'], 'loan_date', row['loan_date'], "loan_date is invalid"])
                        skips.append([row_num, row['employee_number'], row['loan_code'], row['loan_date']])
                        continue

                    lookup_value = row['employee_number'].lower() + row['loan_code'].lower() + row['loan_date']

                    transaction_type = "Add"
                    record = {}
                    if lookup_value in loans:
                        errors.append([row_num, row['employee_number'], 'loan_code', row['loan_code'], "loan already exists"])
                        skips.append([row_num, row['employee_number'], row['loan_code'], row['loan_date']])
                        continue
                    
                    has_missing_field = False
                    for field in REQ_HEADERS:
                        # Check if field in row and not empty
                        if field not in row:
                            errors.append([row_num, row['employee_number'], field, '', field + " required for a new loan"])
                            has_missing_field = True
                            continue

                        if not row[field]:
                            errors.append([row_num, row['employee_number'], field, row[field], field + " required for a new loan"])
                            has_missing_field = True
                            continue

                        if field == 'ded_dur':
                            if row['ded_dur'].lower() not in schedules:
                                errors.append([row_num, row['employee_number'], 'ded_dur', row['ded_dur'], "ded_dur not found in schedules"])
                                has_missing_field = True
                                continue

                    if has_missing_field:
                        skips.append([row_num, row['employee_number'], row['loan_code'], row['loan_date']])
                        continue

                    # If new record, initialize record
                    record['employee_id'] = employees[row['employee_number'].lower()]['id']
                    record['employee_number'] = row['employee_number']
                    record['loan_code_id'] = loan_codes[row['loan_code'].lower()]['id']
                    record['loan_code'] = row['loan_code']
                    record['loan_date'] = row['loan_date']

                    # Get employee record
                    employee = employees[row['employee_number'].lower()]

                    if loan_codes[row['loan_code'].lower()]['is_zero_out']:
                        # Loop in loan for e_empno and l_code and out_bal <>0
                        for loan_key, loan in loans.items():
                            if loan['employee_id'] != record['employee_id']:
                                continue

                            if loan['outstanding_balance'] == 0:
                                continue

                            loan_payment = {
                                'loan_id': loan['id'],
                                'deduction_date': deduction_date,
                                'amount': loan['outstanding_balance'],
                                'outstanding_balance': 0,
                                'is_posted': True,
                                'is_hidden': is_hidden
                            }
                            post_loan_payment_entry(client_db, loan_payment)

                            # Add to zero out list
                            zero_outs.append([loan['employee_number'], loan['loan_code'], loan['loan_date'], loan['outstanding_balance']])

                            loans[loan_key]['outstanding_balance'] = 0.00

                    # Validations
                    # Check employee status
                    has_error = False
                    name = employee['lastname'] + ', ' + employee['firstname'] + ' ' + employee['middlename'][0] + '.' if not employee['suffix'] else employee['lastname'] + ' ' + employee['suffix'] + ', ' + employee['firstname'] + ' ' + employee['middlename'][0]
                    if 'name' in row:
                        if row['name'].upper() != name.upper() and row['name'].upper() != (name.upper() + "."):
                            errors.append([row_num, row['employee_number'], 'name', row['name'], "name is not the same in employee record"])

                    if employee['employment_status_id'] == 0:
                        errors.append([row_num, row['employee_number'], 'employment_status', str(employee['employment_status_id']), "cannot upload loan with this employment status"])
                        has_error = True
                    else:
                        if employment_status[str(employee['employment_status_id'])]['code'] in ['6','7','8','9']:
                            errors.append([row_num, row['employee_number'], 'employment_status', employment_status[str(employee['employment_status_id'])]['code'], "cannot upload loan with this employment status"])
                            has_error = True

                    if row['outstanding_balance'] > row['loan_amount']:
                        errors.append([row_num, row['employee_number'], 'outstanding_balance', row['outstanding_balance'], "outstanding balance should not be greater than the loan amount"])
                        has_error = True

                    if (float(row['installment_amount']) * int(row['no_of_installment'])) > (float(row['loan_amount']) + 1.01):
                        errors.append([row_num, row['employee_number'], 'installment_amount', row['installment_amount'], "installment amount * no of installments should not be greater than the loan amount"])
                        has_error = True

                    if convert_date(row['first_deduction']) is None:
                        errors.append([row_num, row['employee_number'], 'first_deduction', row['first_deduction'], "invalid date"])
                        has_error = True
                    else:
                        if convert_date(row['first_deduction']) < convert_date(row['loan_date']):
                            errors.append([row_num, row['employee_number'], 'first_deduction', row['first_deduction'], "first deduction date should not be earlier than the loan date"])
                            has_error = True

                    if has_error:
                        skips.append([row_num, row['employee_number'], row['loan_code'], row['loan_date']])
                        continue

                    for field in UPDATE_HEADERS:
                        # Check if field in row
                        if field not in row:
                            continue
                        
                        t_code = field
                        tcvalue = row[field]
                        old_value = ""

                        # Fields with reference tables
                        # SCHEDULE_CODE
                        if field == 'ded_dur':
                            t_code = "schedule_id"
                            if tcvalue.lower() not in schedules:
                                errors.append([row_num, row['employee_number'], field, tcvalue, "ded_dur not found in schedules"])
                                continue
                            tcvalue = schedules[tcvalue.lower()]['id']

                        if field == 'first_deduction':
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

                        loans[lookup_value] = record

                        # Insert code here to input audit log
                        audit_log = {
                            'employee_number': row['employee_number'],
                            'tablename':  'loans',
                            'field': t_code,
                            'code': row['loan_code'],
                            'old_value': old_value if type(old_value) is str else str(old_value),
                            'new_value': tcvalue if type(tcvalue) is str else str(tcvalue),
                            'transaction_type': transaction_type,
                            'username': current_user
                        }
                        audit_logs.append(audit_log)
                    
                    if has_update:
                        updated_rows += 1
                    else:
                        skips.append([row_num, row['employee_number'], row['loan_code']])

                data['headers'] = headers
                data['content'] = content
                data['csv_data'] = csv_data
                data['employees'] = employees
                data['audit_logs'] = audit_logs
                data['loans'] = loans

                post_masterfile_audit_logs(data)
                
                # Populate employee_id, loan_code_id, schedule_id
                data['loans'] = array_to_dict_by_keys_lower(populate_field_dict(schedules, data['loans'], 'id', 'schedule_id', 'code', 'schedule_code'), ['employee_number', 'loan_code', 'loan_date'])
                insert_update_loan_entries(data)
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
                'zero_outs': zero_outs,
                'audit_logs': audit_logs
            }, 201
        
        else:
            return {
                'success': success, 
                'errors': errors,
                'message': 'No records updated.',
                'row_count': updated_rows,
                'skips': skips,
                'zero_outs': zero_outs,
                'audit_logs': audit_logs
            }, 200


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def valid_date(date_string):
    try:
        mat = re.match('(\d{4})[-](\d{2})[-](\d{2})$', date_string)
        if mat is not None:
            datetime.datetime.strptime(date_string, "%Y-%m-%d")
            return True
    except ValueError:
        print('ValueError', file=sys.stderr)
        pass
    print('Invalid date', file=sys.stderr)
    return False
