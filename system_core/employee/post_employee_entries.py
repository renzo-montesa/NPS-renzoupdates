from api.v1.employee.model import EmployeeModel
import sys


skip_fields = [
]


check_fields = [
    'branch_id',
    'civil_status_id',
    'nationality_id',
    'rank_id',
    'section_id',
    'employment_status_id',
    'job_type_id',
    'level_id'
]


employee_fields = {
    'id': 'int',
    'branch_id': 'int',
    'employee_number': 'str',
    'swipeno': 'str',
    'firstname': 'str',
    'middlename': 'str',
    'lastname': 'str',
    'suffix': 'str',
    'address': 'str',
    'telephone': 'str',
    'sex': 'str',
    'birthday': 'str',
    'civil_status_id': 'int',
    'nationality_id': 'int',
    'hired_date': 'str',
    'regularization_date': 'str',
    'is_union_member': 'bool',
    'resign_date': 'str',
    'pagibig_additional': 'float',
    'is_pagibig_max': 'bool',
    'rate_min': 'float',
    'rate_hour': 'float',
    'rate_day': 'float',
    'rate_month': 'float',
    'account_number': 'str',
    'timesheet_exempt': 'bool',
    'rank_id': 'int',
    'section_id': 'int',
    'employment_status_id': 'int',
    'job_type_id': 'int',
    'level_id': 'int',
    'pay_type': 'str',
    'pay_code': 'str',
    'gl_account': 'str',
    'supervisor': 'str',
    'ndiff1_rate': 'float',
    'ndiff2_rate': 'float',
    'ot_rate': 'float',
    'tardy_rate': 'float',
    'ut_rate': 'float',
    'absent_rate': 'float',
    'income_out': 'float',
    'cola_rate': 'float',
    'tax_table': 'str',
    'tax_unit': 'str',
    'tax_method': 'str',
    'filed_date': 'str',
    'approved_by': 'str',
    'is_suspended': 'bool',
    'suspend_date': 'str',
    'percentage': 'float',
    'evaluator': 'str',
    'evaluation_date': 'str',
    'old_rate': 'float',
    'old_position': 'str',
    'old_civil_status': 'str',
    'email': 'str',
    'is_inc_alpha': 'bool',
    'is_mwe': 'bool',
    'no_period': 'int',
    'dratemonth': 'float'
}


def post_entry(client_db, employee):
    db_employee, client_session = EmployeeModel.get_by_filter(client_db, employee_number=employee['employee_number'])
    if db_employee:
        update_columns(db_employee, employee)
        client_session.commit()
    else:
        db_employee = EmployeeModel()
        update_columns(db_employee, employee)
        db_employee.save_to_db(client_db)


def insert_update_employee_entries(data):
    for entry_key, employee in data['employees'].items():
        post_entry(data['client_db'], employee)


def update_columns(db_employee, employee):
    for field, value in employee.items():
        if field not in skip_fields:
            if field in employee_fields and value is not None:
                if type(value) is str:
                    print(field + " | " + value, file=sys.stderr)
                if employee_fields[field] == 'str':
                    value = str(value)
                    print(field + " | " + value, file=sys.stderr)
                if employee_fields[field] == 'int':
                    value = int(value)
                    print(field + " | " + str(value), file=sys.stderr)
                if employee_fields[field] == 'float':
                    value = float(value)
                    print(field + " | " + str(value), file=sys.stderr)
                if employee_fields[field] == 'bool':
                    value = bool(int(value))
                    print(field + " | " + str(value), file=sys.stderr)

            if field in check_fields:
                if value == 0:
                    value = None
            setattr(db_employee, field, value)
