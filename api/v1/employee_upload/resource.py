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
from api.v1.csv_map.model import CsvMapModel
from api.v1.masterfile_csv_field.model import MasterfileCsvFieldModel
from api.v1.init_table.model import InitTableModel
from api.v1.init_field.model import InitFieldModel
from api.v1.field_validator.model import FieldValidatorModel
from system_core.helper.array_to_dict import array_to_dict_by_key, array_to_dict_by_keys, array_to_dict_by_key_lower, array_to_dict_by_keys_lower
from system_core.helper.populate_field import populate_field, populate_field_dict
from api.v1.employee.model import EmployeeModel
from api.v1.branch.model import BranchModel
from api.v1.civil_status.model import CivilStatusModel
from api.v1.nationality.model import NationalityModel
from api.v1.rank.model import RankModel
from api.v1.employment_status.model import EmploymentStatusModel
from api.v1.job_type.model import JobTypeModel
from api.v1.level.model import LevelModel
from api.v1.section.model import SectionModel
from api.v1.bank.model import BankModel
from api.v1.employee_bank.model import EmployeeBankModel
from api.v1.previous_employer.model import PreviousEmployerModel
from api.v1.employee_timekeeping.model import EmployeeTimekeepingModel
from api.v1.mandatory_code.model import MandatoryCodeModel
from api.v1.empl_govt_number.model import EmplGovtNumberModel
from system_core.file_writer.write_to_file import write_json_to_file
from system_core.employee.post_employee_entries import insert_update_employee_entries
from system_core.csvconversion.post_audit_logs import post_masterfile_audit_logs
from system_core.employee_bank.post_employee_bank_entries import insert_update_employee_bank_entries
from system_core.previous_employer.post_previous_employer_entries import insert_update_previous_employer_entries
from system_core.employee_timekeeping.post_employee_timekeeping_entries import insert_update_employee_timekeeping_entries
from system_core.empl_govt_number.post_empl_govt_number_entries import insert_update_empl_govt_number_entries
from system_core.helper.convert_date import convert_date
from system_core.helper.data_validator import check_data_type, check_if_empty


GET_EMPLOYEE_UPLOAD = 'get_employee_upload'
POST_EMPLOYEE_UPLOAD = 'post_employee_upload'


ALLOWED_EXTENSIONS = set(['csv'])
UPLOAD_FOLDER = config.UPLOAD_DIR
DATE_FIELDS = [
    'birthday',
    'hired_date',
    'regularization_date',
    'filed_date',
    'suspend_date',
    'evaluation_date'
]


parser = reqparse.RequestParser()
parser.add_argument('file', type=FileStorage, location='files')


class EmployeeUpload(Resource):
    @jwt_required
    @permission_required(GET_EMPLOYEE_UPLOAD)
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
                csv_maps = array_to_dict_by_key_lower(CsvMapModel.get_all(client_db), 'header')

                """Insert code here to convert header to raw_code"""
                for i in range(len(headers)):
                    headers[i] = headers[i].lower()
                    if headers[i] in csv_maps:
                        headers[i] = csv_maps[headers[i]]['raw_code'].lower()

                if 'employee_number' not in headers:
                    errors.append([0, '-', '-', '-', 'EMPLOYEE_NUMBER field is not present in the upload file'])
                    continue

                data = {}
                data['client_db'] = client_db

                csv_fields = MasterfileCsvFieldModel.get_all(client_db)
                csv_data = csv_list_to_dicts(headers, content)
                init_tables = array_to_dict_by_key_lower(InitTableModel.get_all(client_db), 'tablename')
                init_fields = InitFieldModel.get_all(client_db)
                field_validators = array_to_dict_by_keys_lower(FieldValidatorModel.get_all(client_db), ['branch_id','tablename','field'])

                # Company formula
                company = {
                    'month_in_y': 12,
                    'days_in_ye': 262,
                    'hours_in_d': 8,
                    'defa_reg_h': 8,
                    'rate_dform': "round(((rate_month * company['month_in_y']) / company['days_in_ye']), 2)",
                    'ut_formula': "round(((rate_month * company['month_in_y']) / company['days_in_ye']) / company['hours_in_d'], 4)",
                    'tardy_form': "round(((rate_month * company['month_in_y']) / company['days_in_ye']) / company['hours_in_d'], 4)",
                    'absformula': "round(((rate_month * company['month_in_y']) / company['days_in_ye']), 2)",
                    'nd1formula': "round(((rate_month * company['month_in_y']) / company['days_in_ye']) / company['hours_in_d'], 4)",
                    'nd2formula': "round(((rate_month * company['month_in_y']) / company['days_in_ye']) / company['hours_in_d'], 4)",
                    'ot_formula': "round(((rate_month * company['month_in_y']) / company['days_in_ye']) / company['hours_in_d'], 4)",
                    'rate_mform': "round(rate_day / company['defa_reg_h'], 4)"
                }

                employees = array_to_dict_by_key_lower(EmployeeModel.get_all_employees(client_db), 'employee_number')
                branches = array_to_dict_by_key(BranchModel.get_all_by_filter(client_id=client_id), 'branch_code')
                civil_status = array_to_dict_by_key(CivilStatusModel.get_all(client_db), 'code')
                nationality = array_to_dict_by_key(NationalityModel.get_all(client_db), 'code')
                rank = array_to_dict_by_key(RankModel.get_all(client_db), 'code')
                employment_status = array_to_dict_by_key(EmploymentStatusModel.get_all(client_db), 'code')
                job_type = array_to_dict_by_key(JobTypeModel.get_all(client_db), 'code')
                level = array_to_dict_by_key(LevelModel.get_all(client_db), 'code')
                section = array_to_dict_by_key(SectionModel.get_all(client_db), 'code')
                bank = array_to_dict_by_key(BankModel.get_all(client_db), 'bank_code')
                mandatory_code = array_to_dict_by_key(MandatoryCodeModel.get_all(client_db), 'code')
                employee_banks = array_to_dict_by_keys_lower(populate_field(bank, populate_field(employees, EmployeeBankModel.get_all(client_db), 'id', 'employee_id', 'employee_number'), 'id', 'bank_id', 'bank_code'), ['employee_number','bank_code'])
                previous_employers = array_to_dict_by_key_lower(populate_field(employees, PreviousEmployerModel.get_all(client_db), 'id', 'employee_id', 'employee_number'), 'employee_number')
                employee_timekeepings = array_to_dict_by_key_lower(populate_field(employees, EmployeeTimekeepingModel.get_all(client_db), 'id', 'employee_id', 'employee_number'), 'employee_number')
                empl_govt_numbers = array_to_dict_by_keys_lower(populate_field(mandatory_code, populate_field(employees, EmplGovtNumberModel.get_all(client_db), 'id', 'employee_id', 'employee_number'), 'id', 'mandatory_code_id', 'code', 'mandatory_code'), ['employee_number','mandatory_code'])
                audit_logs = []
                row_num = 1

                for row in csv_data:
                    row_num += 1
                    has_update = False
                    transaction_type = "Add"

                    if row['employee_number'] == "":
                        skips.append([row_num, row['employee_number']])
                        continue

                    employee_number = row['employee_number'].lower()

                    if employee_number in employees:
                        transaction_type = "Edit"
                        branch_id = employees[employee_number]['branch_id']
                    
                    else:
                        if 'branch_code' not in row:
                            errors.append([row_num, row['employee_number'], 'branch_code', '', "branch_code required for new employees"])
                            skips.append([row_num, row['employee_number']])
                            continue

                        if row['branch_code'] not in branches:
                            errors.append([row_num, row['employee_number'], 'branch_code', row['branch_code'], "branch_code not found in branches"])
                            skips.append([row_num, row['employee_number']])
                            continue

                        branch_id = branches[row['branch_code']]['id']

                    # Check required fields
                    missing_fields = []
                    invalid_fields = []
                    for field_key, field_validator in field_validators.items():
                        if transaction_type == "Add" and field_validator['branch_id'] == branch_id and field_validator['is_req_new']:
                            if field_validator['field'] not in row:
                                print("Add Required field: " + field_validator['field'], file=sys.stderr)
                                missing_fields.append(field_validator['field'])
                                continue
                            if check_if_empty(row[field_validator['field']], field_validator['data_type']):
                                errors.append([row_num, row['employee_number'], field_validator['field'], row[field_validator['field']], "invalid value"])
                                invalid_fields.append(field_validator['field'])
                                continue
                            if field_validator['data_type'] == 'str' and field_validator['valid_length'] > 0:
                                if len(row[field_validator['field']]) > field_validator['valid_length']:
                                    errors.append([row_num, row['employee_number'], field_validator['field'], row[field_validator['field']], "invalid length"])
                                    invalid_fields.append(field_validator['field'])
                                    continue
                        if transaction_type == "Edit" and field_validator['branch_id'] == branch_id and field_validator['is_req_exist'] and field_validator['field'] not in row:
                            print("Edit Required field: " + field_validator['field'], file=sys.stderr)
                            missing_fields.append(field_validator['field'])
                            continue

                    # Validate dates
                    for field in DATE_FIELDS:
                        if field in row:
                            tcvalue = convert_date(row[field])
                            if tcvalue is None:
                                errors.append([row_num, row['employee_number'], field, row[field], "invalid date"])
                                invalid_fields.append(field)
                                continue

                    if len(missing_fields) > 0 or len(invalid_fields) > 0:
                        if len(missing_fields) > 0:
                            errors.append([row_num, row['employee_number'], '', '', "Missing fields: " + ','.join(missing_fields)])
                        if len(invalid_fields) > 0:
                            errors.append([row_num, row['employee_number'], '', '', "Invalid value in fields: " + ','.join(invalid_fields)])
                        skips.append([row_num, row['employee_number']])
                        continue

                    for csv_field in csv_fields:
                        print("passed here, inside csv_fields loop", file=sys.stderr)
                        raw_code = csv_field['raw_code'].lower()
                        code = csv_field['code'].lower()
                        tablename = csv_field['tablename'].lower()
                        t_code = csv_field['t_code'].lower()

                        if raw_code not in row:
                            #print("passed here, raw_code not in row", file=sys.stderr)
                            continue

                        if not row[raw_code]:
                            #print("passed here, not row[raw_code]", file=sys.stderr)
                            continue

                        #if tablename == 'employees':
                        #    print("passed here, tablename == employees", file=sys.stderr)
                        #    continue

                        # Insert code here to get filter in init_tables
                        if tablename not in init_tables:
                            #print("passed here, tablename not in init_tables", file=sys.stderr)
                            continue

                        # Skip fields not to employees
                        if tablename not in ["employees","employee_banks","previous_employers","employee_timekeepings","empl_govt_numbers"]:
                            continue

                        # Insert code here to fix data type of value and evaluate formula
                        print("passed here, fix data type", file=sys.stderr)
                        tcvalue = row[raw_code]

                        # Catch formula error
                        try:
                            tcvalue = eval(csv_field['formula'])
                        except:
                            errors.append([row_num, row['employee_number'], raw_code, tcvalue, "error encountered in formula"])
                            continue

                        # Check value if valid data type and length
                        validator_key = str(branch_id) + tablename + raw_code
                        if validator_key in field_validators:
                            if field_validators[validator_key]['auto_replace'] is not None and field_validators[validator_key]['auto_replace'] != '':
                                tcvalue = field_validators[validator_key]['auto_replace']
                            is_valid_data, data_error = check_data_type(tcvalue, field_validators[validator_key]['data_type'])
                            # Check data type
                            if not is_valid_data:
                                errors.append([row_num, row['employee_number'], raw_code, tcvalue, data_error])
                                continue
                            # Check length
                            if field_validators[validator_key]['data_type'] == 'str' and field_validators[validator_key]['valid_length'] > 0:
                                if len(tcvalue) > field_validators[validator_key]['valid_length']:
                                    errors.append([row_num, row['employee_number'], raw_code, tcvalue, "Invalid length"])
                                    continue
                            # Check condition
                            if field_validators[validator_key]['condition']:
                                try:
                                    if not eval(field_validators[validator_key]['condition']):
                                        errors.append([row_num, row['employee_number'], raw_code, tcvalue, "value did not meet the condition"])
                                        continue
                                except Exception as e:
                                    errors.append([row_num, row['employee_number'], raw_code, tcvalue, "error evaluating condition"])
                                    continue

                        # Fields with reference tables
                        # BRANCH
                        if code == 'branch_code':
                            if tcvalue not in branches:
                                errors.append([row_num, row['employee_number'], raw_code, tcvalue, "branch_code not found in branches"])
                                break
                            tcvalue = branches[tcvalue]['id']

                        # CIVIL STATUS
                        if code == 'civil_status_code':
                            if tcvalue not in civil_status:
                                errors.append([row_num, row['employee_number'], raw_code, tcvalue, "code not found in civil_status"])
                                continue
                            tcvalue = civil_status[tcvalue]['id']

                        # NATIONALITY
                        if code == 'nationality_code':
                            if tcvalue not in nationality:
                                errors.append([row_num, row['employee_number'], raw_code, tcvalue, "code not found in nationality"])
                                continue
                            tcvalue = nationality[tcvalue]['id']

                        # RANK
                        if code == 'rank_code':
                            if tcvalue not in rank:
                                errors.append([row_num, row['employee_number'], raw_code, tcvalue, "code not found in rank"])
                                continue
                            tcvalue = rank[tcvalue]['id']

                        # EMPLOYMENT STATUS
                        if code == 'employment_status_code':
                            if tcvalue not in employment_status:
                                errors.append([row_num, row['employee_number'], raw_code, tcvalue, "code not found in employment_status"])
                                continue
                            tcvalue = employment_status[tcvalue]['id']
                        
                        # JOB TYPE
                        if code == 'job_type_code':
                            if tcvalue not in job_type:
                                errors.append([row_num, row['employee_number'], raw_code, tcvalue, "code not found in job_type"])
                                continue
                            tcvalue = job_type[tcvalue]['id']

                        # LEVEL
                        if code == 'level_code':
                            if tcvalue not in level:
                                errors.append([row_num, row['employee_number'], raw_code, tcvalue, "code not found in level"])
                                continue
                            tcvalue = level[tcvalue]['id']

                        # SECTION
                        if code == 'section_code':
                            if tcvalue not in section:
                                errors.append([row_num, row['employee_number'], raw_code, tcvalue, "code not found in section"])
                                continue
                            tcvalue = section[tcvalue]['id']

                        #BANK CODE
                        if code == 'bank_code':
                            if tcvalue not in bank:
                                errors.append([row_num, row['employee_number'], raw_code, tcvalue, "code not found in bank"])
                                continue
                            tcvalue = bank[tcvalue]['id']

                        # Account_number should have bank_code
                        if code == 'account_number':
                            if 'bank_code' not in row:
                                errors.append([row_num, row['employee_number'], raw_code, tcvalue, "invalid bank code for account_number"])
                                continue
                            if row['bank_code'] not in bank:
                                continue

                        # Validate dates
                        if t_code in DATE_FIELDS:
                            if tcvalue:
                                tcvalue = convert_date(tcvalue)
                                if tcvalue is None:
                                    errors.append([row_num, row['employee_number'], raw_code, row[raw_code], "invalid date"])
                                    continue

                        filters = list(init_tables[tablename]['filter'].split(","))

                        lookup_value = ""
                        for filter_field in filters:
                            filter_field = list(filter_field.split('.'))
                            filter_field = filter_field[0] if len(filter_field) < 2 else (filter_field[0] + "['" + filter_field[1] + "']")
                            filter_value = eval(filter_field)
                            print(filter_value, file=sys.stderr)
                            lookup_value += filter_value.lower() if type(filter_value) is str else str(filter_value).lower()

                        """Insert code here to locate record in table"""
                        old_value = ""
                        record = {}
                        if lookup_value in eval(tablename):
                            record = eval(tablename + "['" + lookup_value + "']")
                            if t_code in record:
                                old_value = record[csv_field['t_code'].lower()]
                        else:
                            """If new record, insert code here to initialize record"""
                            for init_field in init_fields:
                                if init_field['tablename'].lower() != tablename:
                                    print("passed here, init_field['tablename'] != tablename | " + init_field['tablename'], file=sys.stderr)
                                    continue
                                record[init_field['field'].lower()] = eval(init_field['value'])

                        print("passed here, " + record['employee_number'], file=sys.stderr)
                        print("passed here, tcvalue | " + str(tcvalue), file=sys.stderr)
                        print("passed here, t_code | " + t_code, file=sys.stderr)

                        # COMPUTE RATES
                        if code == 'rate_month' or code == 'rate_day':
                            rate_month = 0.00
                            rate_day = 0.00
                            try:
                                if code == 'rate_month':
                                    rate_month = float(tcvalue)
                                    if rate_month == 0.0:
                                        errors.append([row_num, row['employee_number'], raw_code, tcvalue, "rate month should not be empty"])
                                        continue
                                    exec("record['rate_day'] = " + company['rate_dform'])
                                    rate_day = record['rate_day']

                                if code == 'rate_day':
                                    rate_month = record['rate_month']
                                    rate_day = float(tcvalue)
                                    if rate_month == 0.0:
                                        errors.append([row_num, row['employee_number'], raw_code, tcvalue, "rate month should not be empty"])
                                        continue
                            except Exception as e:
                                errors.append([row_num, row['employee_number'], raw_code, tcvalue, str(e)])
                                continue

                            exec("record['rate_hour'] = " + company['rate_mform'])
                            rate_hour = record['rate_hour']
                            record['rate_min'] = round(rate_hour / 60, 4)
                            exec("record['ut_rate'] = " + company['ut_formula'])
                            exec("record['tardy_rate'] = " + company['tardy_form'])
                            exec("record['absent_rate'] = " + company['absformula'])
                            exec("record['ndiff1_rate'] = " + company['nd1formula'])
                            exec("record['ndiff2_rate'] = " + company['nd2formula'])
                            exec("record['ot_rate'] = " + company['ot_formula'])

                        print("passed here, tcvalue | " + str(tcvalue), file=sys.stderr)

                        if t_code in record:
                            """Insert code here to check if string to numeric is not 0 or empty"""
                            print("passed here, check data type | " + t_code + " | " + type(record[t_code]).__name__, file=sys.stderr)
                            try:
                                if type(record[t_code]) is str:
                                    tcvalue = str(tcvalue)
                                if type(record[t_code]) is int:
                                    tcvalue = int(tcvalue)
                                if type(record[t_code]) is float:
                                    tcvalue = float(tcvalue)
                                if type(record[t_code]) is bool:
                                    tcvalue = bool(int(tcvalue))
                            except Exception as e:
                                errors.append([row_num, row['employee_number'], raw_code, tcvalue, str(e)])
                                continue

                            if record[t_code] == tcvalue:
                                print("passed here, record[t_code] == tcvalue", file=sys.stderr)
                                #print(record[t_code] + " == " + tcvalue, file=sys.stderr)
                                continue

                        """Insert code here to update column with value"""
                        print("passed here, record[t_code] = tcvalue | " + t_code, file=sys.stderr)
                        record[t_code] = tcvalue
                        has_update = True

                        print("passed here, " + tablename + "['" + lookup_value + "'] = record", file=sys.stderr)
                        exec(tablename + "['" + lookup_value + "'] = record")

                        """Insert code here to input audit log"""
                        audit_log = {
                            'employee_number': row['employee_number'],
                            'tablename':  tablename,
                            'field': csv_field['t_code'],
                            'code': csv_field['code'],
                            'old_value': old_value if type(old_value) is str else str(old_value),
                            'new_value': tcvalue if type(tcvalue) is str else str(tcvalue),
                            'transaction_type': transaction_type,
                            'username': current_user
                        }
                        audit_logs.append(audit_log)
                        print("passed here, added audit_log", file=sys.stderr)
                    
                    if has_update:
                        updated_rows += 1
                    else:
                        skips.append([row_num, row['employee_number']])

                data['csv_fields'] = csv_fields
                data['headers'] = headers
                data['content'] = content
                data['csv_data'] = csv_data
                data['init_tables'] = init_tables
                data['init_fields'] = init_fields
                data['employees'] = employees
                data['audit_logs'] = audit_logs
                data['employee_banks'] = employee_banks
                data['employee_timekeepings'] = employee_timekeepings
                data['empl_govt_numbers'] = empl_govt_numbers

                post_masterfile_audit_logs(data)
                insert_update_employee_entries(data)

                # Get employee ids
                employee_ids = array_to_dict_by_key_lower(EmployeeModel.get_all_ids(client_db), 'employee_number')

                # Populate employee_id
                data['employee_banks'] = array_to_dict_by_keys_lower(populate_field_dict(employee_ids, employee_banks, 'employee_number', 'employee_number', 'id', 'employee_id'), ['employee_number','bank_code'])
                insert_update_employee_bank_entries(data)

                # Populate employee_id
                data['previous_employers'] = array_to_dict_by_key_lower(populate_field_dict(employee_ids, previous_employers, 'employee_number', 'employee_number', 'id', 'employee_id'), 'employee_number')
                insert_update_previous_employer_entries(data)

                # Populate employee_id
                data['employee_timekeepings'] = array_to_dict_by_key_lower(populate_field_dict(employee_ids, employee_timekeepings, 'employee_number', 'employee_number', 'id', 'employee_id'), 'employee_number')
                insert_update_employee_timekeeping_entries(data)

                # Populate employee_id and mandatory_code_id
                data['empl_govt_numbers'] = array_to_dict_by_keys_lower(populate_field(mandatory_code, populate_field_dict(employee_ids, empl_govt_numbers, 'employee_number', 'employee_number', 'id', 'employee_id'), 'code', 'mandatory_code', 'id', 'mandatory_code_id'), ['employee_number','mandatory_code'])
                insert_update_empl_govt_number_entries(data)

                #write_json_to_file(data)
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
