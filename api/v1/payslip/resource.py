from flask import request
from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.v1.user_role_permission_info.model import UserRolePermissionInfoModel, permission_required
from api.v1.client.model import ClientModel
from api.v1.payslip_info.model import PayslipInfoModel
from api.v1.payslip_entry_type_info.model import PayslipEntryTypeInfoModel


GET_PAYSLIP = 'get_payslip'
ADD_PAYSLIP = 'add_payslip'
EDIT_PAYSLIP = 'edit_payslip'
DELETE_PAYSLIP = 'delete_payslip'


payslip_args = {
    'id': fields.Int(),
    'employee_id': fields.Int(),
    'employee_number': fields.Str(),
    'firstname': fields.Str(),
    'middlename': fields.Str(),
    'lastname': fields.Str(),
    'payroll_period_id': fields.Int(),
    'period_start': fields.Str(),
    'period_end': fields.Str(),
    'transaction_start': fields.Str(),
    'transaction_end': fields.Str(),
    'earnings': fields.Float(),
    'deductions': fields.Float(),
    'net_pay': fields.Float(),
    'take_home': fields.Float()
}

payslip_fields = {
    'id': mfields.Integer,
    'employee_id': mfields.Integer,
    'employee_number': mfields.String,
    'firstname': mfields.String,
    'middlename': mfields.String,
    'lastname': mfields.String,
    'payroll_period_id': mfields.Integer,
    'period_start': mfields.String,
    'period_end': mfields.String,
    'transaction_start': mfields.String,
    'transaction_end': mfields.String,
    'earnings': mfields.Float,
    'deductions': mfields.Float,
    'basic_pay': mfields.Float,
    'w_tax': mfields.Float,
    'empl_sss': mfields.Float,
    'prov_ee': mfields.Float,
    'empl_med': mfields.Float,
    'empl_pagib': mfields.Float,
    'net_pay': mfields.Float,
    'take_home': mfields.Float
}

payslip_list_fields = {
    'payslips': mfields.List(mfields.Nested(payslip_fields))
}


class Payslip(Resource):
    @jwt_required
    @permission_required(GET_PAYSLIP)
    @use_args(payslip_args)
    def get(self, args, payslip_id=None):
        client_id = request.args.get('client_id')
        client = ClientModel.query.get(client_id)
        if client:
            client_db = client.db_name
        else:
            return {
                'success': False,
                'message': 'Client not found'
            }, 401

        
        if 'payroll_period_id' in args:
            payslips = PayslipInfoModel.get_all_by_filter(client_db, payroll_period_id=args['payroll_period_id'])

            for i in range(len(payslips)):
                payslips[i]['earnings'] = PayslipEntryTypeInfoModel.get_total_earnings_by_payslip_id(client_db, payslips[i]['id'])
                payslips[i]['deductions'] = PayslipEntryTypeInfoModel.get_total_deductions_by_payslip_id(client_db, payslips[i]['id'])
                payslips[i]['basic_pay'] = PayslipEntryTypeInfoModel.get_sum_by_filter(client_db, payslip_id=payslips[i]['id'], pay_element_code="basic_pay")
                payslips[i]['w_tax'] = PayslipEntryTypeInfoModel.get_sum_by_filter(client_db, payslip_id=payslips[i]['id'], pay_element_code="w_tax")
                payslips[i]['empl_sss'] = PayslipEntryTypeInfoModel.get_sum_by_filter(client_db, payslip_id=payslips[i]['id'], pay_element_code="empl_sss")
                payslips[i]['prov_ee'] = PayslipEntryTypeInfoModel.get_sum_by_filter(client_db, payslip_id=payslips[i]['id'], pay_element_code="prov_ee")
                payslips[i]['empl_med'] = PayslipEntryTypeInfoModel.get_sum_by_filter(client_db, payslip_id=payslips[i]['id'], pay_element_code="empl_med")
                payslips[i]['empl_pagib'] = PayslipEntryTypeInfoModel.get_sum_by_filter(client_db, payslip_id=payslips[i]['id'], pay_element_code="empl_pagib")
            
            return marshal({
                'payslips': payslips
            }, payslip_list_fields)

        elif payslip_id:
            payslip = marshal(PayslipInfoModel.get_by_filter(id=payslip_id), payslip_fields)

            payslip['earnings'] = PayslipEntryTypeInfoModel.get_total_earnings_by_payslip_id(client_db, payslip['id'])
            payslip['deductions'] = PayslipEntryTypeInfoModel.get_total_deductions_by_payslip_id(client_db, payslip['id'])
            
            return payslip

        else:
            return {'message': 'Unauthorized access'}, 403
