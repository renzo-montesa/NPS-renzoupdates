from api.v1.employee_info.model import EmployeeInfoModel
from flask_restful import marshal, fields as mfields
from system_core.helper.array_to_dict import (array_to_dict_by_key)


employee_fields = {
    'id': mfields.Integer,
    'branch_id': mfields.Integer,
    'employee_number': mfields.String,
    'firstname': mfields.String,
    'middlename': mfields.String,
    'lastname': mfields.String,
    'telephone': mfields.String,
    'sex': mfields.String,
    'birthday': mfields.String,
    'civil_status_id': mfields.Integer,
    'civil_status_code': mfields.String,
    'civil_status_description': mfields.String,
    'nationality_id': mfields.Integer,
    'nationality_code': mfields.String,
    'nationality_description': mfields.String,
    'hired_date': mfields.String,
    'regularization_date': mfields.String,
    'pagibig_additional': mfields.Float,
    'is_pagibig_max': mfields.Boolean,
    'rate_hour': mfields.Float,
    'rate_day': mfields.Float,
    'rate_month': mfields.Float,
    'timesheet_exempt': mfields.Boolean,
    'rank_id': mfields.Integer,
    'rank_code': mfields.String,
    'rank_description': mfields.String,
    'section_id': mfields.Integer,
    'section_code': mfields.String,
    'section_description': mfields.String,
    'department_id': mfields.Integer,
    'department_code': mfields.String,
    'department_description': mfields.String,
    'employment_status_id': mfields.Integer,
    'employment_status_code': mfields.String,
    'employment_status_description': mfields.String,
    'job_type_id': mfields.Integer,
    'job_type_code': mfields.String,
    'job_type_description': mfields.String,
    'level_id': mfields.Integer,
    'level_code': mfields.String,
    'level_description': mfields.String,
    'pay_type': mfields.String,
    'pay_code': mfields.String
}


def get_active_employees(data):
    data['employees'] = {}

    data['employees'] = array_to_dict_by_key(EmployeeInfoModel.get_active_employees(data['client_db']), 'id')

    for entry_key, employee in data['employees'].items():
        data['employees'][entry_key]['sss_basis'] = 'G'
        data['employees'][entry_key]['med_basis'] = 'G'
