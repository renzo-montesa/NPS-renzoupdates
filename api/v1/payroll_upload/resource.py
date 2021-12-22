from flask import request, jsonify
import flask
from sqlalchemy.sql.expression import update
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required)
from flask_jwt_extended import decode_token,get_jwt_identity
from webargs import fields
from webargs.flaskparser import use_args
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
from api.v1.csv_map.model import CsvMapModel
from api.v1.csv_field.model import CsvFieldModel
from api.v1.init_table.model import InitTableModel
from api.v1.init_field.model import InitFieldModel
from system_core.helper.array_to_dict import array_to_dict_by_key, array_to_dict_by_keys, array_to_dict_by_key_lower, array_to_dict_by_keys_lower
from api.v1.employee_info.model import EmployeeInfoModel
from api.v1.payslip_entry_detail.model import PayslipEntryDetailModel
from api.v1.timekeeping_detail.model import TimekeepingDetailModel
from system_core.file_writer.write_to_file import write_json_to_file
from api.v1.pay_element_info.model import PayElementInfoModel
from api.v1.tk_element_info.model import TkElementInfoModel
from api.v1.csv_audit_log.model import CsvAuditLogModel
from system_core.payslip_entry.post_payslip_entries import insert_update_payslip_entries
from system_core.timekeeping.post_timekeepings import insert_update_timekeepings
from system_core.csvconversion.post_audit_logs import post_audit_logs
from api.v1.payslip_info.model import PayslipInfoModel



GET_PAYROLL_UPLOAD = 'get_payroll_upload'
POST_PAYROLL_UPLOAD = 'post_payroll_upload'

ALLOWED_EXTENSIONS = set(['txt', 'csv'])
UPLOAD_FOLDER = config.UPLOAD_DIR


parser = reqparse.RequestParser()
parser.add_argument('file', type=FileStorage, location='files')


class PayrollUpload(Resource):
    @jwt_required
    @permission_required(GET_PAYROLL_UPLOAD)
    def get(self, args):
        return {"message": "GET"}, 200
    
    def post(self):
        

        #gets username from token
        headers = flask.request.headers
        bearer = headers.get('Authorization')    # Bearer YourTokenHere
        token = bearer.split()[1]  # YourTokenHere
        decodedtoken=decode_token(token)
        
        
        files = request.files.getlist('file')
        client_id = request.form.get('compid')
        payroll_period_id = request.form.get('payprdid')

        client = ClientModel.query.get(client_id)
        if client:
            client_db = client.db_name
        else:
            return {
                'success': False,
                'message': 'File uploading failed.',
                'errors': [['-', '-', '-', 'Client not found']],
                'skips': [],
                'audit_logs': [],
                'row_count': 0
            }, 200

        client.close()

        success = True
        errors = []
        update_logs = []
        skips = []
        rowCount = 0
        
        for file in files:
            if file and allowed_file(file.filename):
                file_uid = uuid.uuid1().hex
                filename = secure_filename(file.filename)
                fullpath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(fullpath)

                upload_file = UploadFileModel(file_uid=file_uid, fullpath=fullpath, filename=filename)
                upload_file.save_to_db()
                upload_file.close()

                headers, duplicate_headers = get_headers(fullpath)
                
                if len(duplicate_headers) > 0:
                    errors.append([file.filename, '', '', 'File has duplicate headers: ' + ', '.join(duplicate_headers)])
                    continue
                
                content = get_content(fullpath)
                csv_maps = array_to_dict_by_key_lower(CsvMapModel.get_all(client_db), 'header')


                """Insert code here to convert header to raw_code"""
                for i in range(len(headers)):
                    headers[i] = headers[i].lower()
                    if headers[i] in csv_maps:
                        headers[i] = csv_maps[headers[i]]['raw_code'].lower()

                if 'employee_number' not in headers:
                    errors.append([file.filename, '', '', 'EMPLOYEE_NUMBER is not present in the upload file'])
                    continue

                data = {}

                csv_fields = CsvFieldModel.get_all(client_db)
                csv_data = csv_list_to_dicts(headers, content)
                init_tables = array_to_dict_by_key_lower(InitTableModel.get_all(client_db), 'tablename')
                init_fields = InitFieldModel.get_all(client_db)

               
                employees = array_to_dict_by_key(EmployeeInfoModel.get_all_employees(client_db), 'employee_number')
                payslip_info=array_to_dict_by_keys_lower(PayslipInfoModel.get_payslips_by_payroll_period_id(client_db,payroll_period_id),['employee_number','payroll_period_id'])
                payslip_entries = array_to_dict_by_keys_lower(PayslipEntryDetailModel.get_all_by_payroll_period_id(client_db, payroll_period_id), ['employee_number','payroll_period_id','pay_element_code'])
                timekeepings = array_to_dict_by_keys_lower(TimekeepingDetailModel.get_all_by_payroll_period_id(client_db, payroll_period_id), ['employee_number','payroll_period_id','tk_element_code'])
                pay_elements = array_to_dict_by_key(PayElementInfoModel.get_pay_elements(client_db), 'pay_element_code')
                tk_elements = array_to_dict_by_key(TkElementInfoModel.get_tk_elements(client_db), 'tk_element_code')
                audit_logs = []
                row_num = 1

                for row in csv_data:
                    row_num += 1
                    rowCount += 1
                    has_update = False

                    print("passed here, before check employee_number", file=sys.stderr)
                    if row['employee_number'] not in employees:
                        errors.append([file.filename, row_num, row['employee_number'], 'Employee does not exist'])
                        skips.append([file.filename, row_num, row['employee_number']])
                        continue

                    employee = employees[row['employee_number'].lower()]
                    middle_initial = "" if not employee['middlename'] else employee['middlename'][0]
                    name = employee['lastname'] + ', ' + employee['firstname'] + ' ' + middle_initial if not employee['suffix'] else employee['lastname'] + ' ' + employee['suffix'] + ', ' + employee['firstname'] + ' ' + middle_initial
                    if 'name' in row:
                        if row['name'].upper() != name.upper() and row['name'].upper() != (name.upper() + "."):
                            errors.append([file.filename, row_num, row['employee_number'], 'Name does not match in masterfile'])

                    for csv_field in csv_fields:
                        print("passed here, inside csv_fields loop", file=sys.stderr)
                        raw_code = csv_field['raw_code'].lower()
                        tablename = csv_field['tablename'].lower()
                        t_code = csv_field['t_code'].lower()

                        if raw_code not in row:
                            print("passed here, raw_code not in row", file=sys.stderr)
                            continue

                        if not row[raw_code]:
                            print("passed here, not row[raw_code]", file=sys.stderr)
                            continue

                        if tablename == 'employees':
                            print("passed here, tablename == employees", file=sys.stderr)
                            continue

                        """Insert code here to get filter in init_tables"""
                        if tablename not in init_tables:
                            print("passed here, tablename not in init_tables", file=sys.stderr)
                            continue

                        filters = list(init_tables[tablename]['filter'].split(","))

                        lookup_value = ""
                        for filter_field in filters:
                            filter_field = list(filter_field.split('.'))
                            filter_field = filter_field[0] if len(filter_field) < 2 else (filter_field[0] + "['" + filter_field[1] + "']")
                            filter_value = eval(filter_field)
                            print(filter_value, file=sys.stderr)
                            lookup_value += filter_value.lower() if type(filter_value) is str else str(filter_value).lower()

                        """Insert code here to fix data type of value and evaluate formula"""
                        tcvalue = row[raw_code]
                        try:
                            tcvalue = eval(csv_field['formula'])
                        except Exception as e:
                            errors.append([file.filename, row_num, row['employee_number'], 'Raw Code: ' + raw_code + ' | Error in formula'])
                            continue

                        """Insert code here to locate record in table"""
                        transaction_type = "Add"
                        old_value = ""
                        record = {}
                        if lookup_value in eval(tablename):
                            record = eval(tablename + "['" + lookup_value + "']")
                            transaction_type = "Edit"
                            old_value = record[csv_field['t_code'].lower()]
                        else:
                            """If new record, insert code here to initialize record"""
                            for init_field in init_fields:
                                if init_field['tablename'].lower() != tablename:
                                    print("passed here, init_field['tablename'] != tablename", file=sys.stderr)
                                    continue
                                try:
                                    record[init_field['field'].lower()] = eval(init_field['value'])
                                except Exception as e:
                                    errors.append([file.filename, row_num, row['employee_number'], 'Raw Code: ' + raw_code + ' | Error in init_field value'])

                        """Insert code here to check if value is still the same"""
                        print("passed here, tcvalue", file=sys.stderr)
                        print(tcvalue, file=sys.stderr)
                        if t_code in record:
                            try:
                                if type(record[t_code]) is str:
                                    tcvalue = str(tcvalue)
                                if type(record[t_code]) is int:
                                    tcvalue = int(tcvalue)
                                if type(record[t_code]) is float:
                                    tcvalue = float(tcvalue)
                                if type(record[t_code]) is bool:
                                    tcvalue = bool(tcvalue)

                                if record[t_code] == tcvalue:
                                    print("passed here, record[t_code] == tcvalue", file=sys.stderr)
                                    continue
                            except Exception as e:
                                errors.append([file.filename, row_num, row['employee_number'], 'Raw Code: ' + raw_code + ' | ' + str(e)])
                                continue

                        """Insert code here to update column with value"""
                        record[t_code] = tcvalue

                        exec(tablename + "['" + lookup_value + "'] = record")
                        has_update = True

                        """Insert code here to input audit log"""
                        audit_log = {
                            'filename': file.filename,
                            'row_no': row_num,
                            'employee_number': row['employee_number'],
                            'payroll_period_id': payroll_period_id,
                            'tablename':  tablename,
                            'field': csv_field['t_code'],
                            'code': csv_field['code'],
                            'old_value': old_value if type(old_value) is str else str(old_value),
                            'new_value': tcvalue if type(tcvalue) is str else str(tcvalue),
                            'transaction_type': transaction_type,
                            'username': decodedtoken['identity']
                        }
                        audit_logs.append(audit_log)
                        print("passed here, added audit_log", file=sys.stderr)

                    if not has_update:
                        skips.append([file.filename, row_num, row['employee_number']])

                data['client_db'] = client_db
                data['payroll_period_id'] = payroll_period_id
                data['csv_fields'] = csv_fields
                data['headers'] = headers
                data['content'] = content
                data['csv_data'] = csv_data
                data['init_tables'] = init_tables
                data['init_fields'] = init_fields
                data['employees'] = employees
                data['payslip_entries'] = payslip_entries
                data['timekeepings'] = timekeepings
                data['pay_elements'] = pay_elements
                data['tk_elements'] = tk_elements
                data['audit_logs'] = audit_logs
                data['payslip_info']=payslip_info

                update_logs += audit_logs

                insert_update_payslip_entries(data)
                insert_update_timekeepings(data)
                post_audit_logs(data)
            else:
                errors.append([file.filename, '', '', 'File type is not allowed'])
                continue

        if success:
            message = 'File uploaded successfully.' if len(errors)==0 else 'File uploaded successfully but with errors.'
            message = message if len(update_logs)>0 else 'No records updated.'
            return {
                'success': success,
                'message': message,
                'errors': errors,
                'skips': skips,
                'audit_logs': update_logs,
                'row_count': rowCount,
                'username':decodedtoken['identity']
            }, 200
        else:
            return {
                'success': success,
                'message': 'No records updated.',
                'errors': errors,
                'skips': skips,
                'audit_logs': update_logs,
                'row_count': 0
            }, 200

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
