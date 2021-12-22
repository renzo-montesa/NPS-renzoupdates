from flask import request
from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from webargs.flaskparser import use_args
from api.v1.payroll_period.model import PayrollPeriodModel
from api.v1.client.model import ClientModel
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.v1.user_role_permission_info.model import UserRolePermissionInfoModel, permission_required


GET_PAYROLL_PERIOD = 'get_payroll_period'
ADD_PAYROLL_PERIOD = 'add_payroll_period'
EDIT_PAYROLL_PERIOD = 'edit_payroll_period'
DELETE_PAYROLL_PERIOD = 'delete_payroll_period'


payroll_period_args = {
    'id': fields.Int(),
    'branch_id': fields.Int(),
    'schedule_id': fields.Int(),
    'period_start': fields.Str(),
    'period_end': fields.Str(),
    'transaction_start': fields.Str(),
    'transaction_end': fields.Str(),
    'type': fields.Str(),
    'is_summarized': fields.Bool(),
    'is_locked': fields.Bool(),
    'is_hidden': fields.Bool()
}

payroll_period_fields = {
    'id': mfields.Integer,
    'branch_id': mfields.Integer,
    'schedule_id': mfields.Integer,
    'period_start': mfields.String,
    'period_end': mfields.String,
    'transaction_start': mfields.String,
    'transaction_end': mfields.String,
    'type': mfields.String,
    'is_summarized': mfields.Boolean,
    'is_locked': mfields.Boolean,
    'is_hidden': mfields.Boolean
}

payroll_period_list_fields = {
    'count': mfields.Integer,
    'payroll_periods': mfields.List(mfields.Nested(payroll_period_fields))
}


class PayrollPeriod(Resource):
    @jwt_required
    @permission_required(GET_PAYROLL_PERIOD)
    @use_args(payroll_period_args)
    def get(self, args, payroll_period_id=None):
        client_id = request.args.get('client_id')
        client = ClientModel.query.get(client_id)
        if client:
            client_db = client.db_name
        else:
            return {
                'success': False,
                'message': 'Client not found'
            }, 401

        if payroll_period_id:
            payroll_period = PayrollPeriodModel.get_by_filter(client_db, id=payroll_period_id)

            return payroll_period

        else:
            payroll_periods = PayrollPeriodModel.get_all(client_db)

            return {
                'count': len(payroll_periods),
                'payroll_periods': payroll_periods
            }
    
    @jwt_required
    @permission_required(ADD_PAYROLL_PERIOD)
    @use_args(payroll_period_args)
    def post(self, args):
        payroll_period = PayrollPeriodModel(**args)

        try:
            payroll_period.save_to_db()

            return marshal(payroll_period, payroll_period_fields)
        except Exception as e:
            return {'message': 'Error: ' + str(e)}, 500

    @jwt_required
    @permission_required(EDIT_PAYROLL_PERIOD)
    @use_args(payroll_period_args)
    def put(self, args, payroll_period_id=None):
        payroll_period = PayrollPeriodModel.query.get(payroll_period_id)

        if payroll_period:
            if 'branch_id' in args:
                payroll_period.branch_id = args['branch_id']
            if 'schedule_id' in args:
                payroll_period.schedule_id = args['schedule_id']
            if 'period_start' in args:
                payroll_period.period_start = args['period_start']
            if 'period_end' in args:
                payroll_period.period_end = args['period_end']
            if 'transaction_start' in args:
                payroll_period.transaction_start = args['transaction_start']
            if 'transaction_end' in args:
                payroll_period.transaction_end = args['transaction_end']
            if 'is_summarized' in args:
                payroll_period.is_summarized = args['is_summarized']
            if 'is_locked' in args:
                payroll_period.is_locked = args['is_locked']
            if 'is_hidden' in args:
                payroll_period.is_hidden = args['is_hidden']
            
            payroll_period.commit_to_db()

            return marshal(payroll_period, payroll_period_fields)
        else:
            return {'message': 'Record not found.'}, 200

    @jwt_required
    @permission_required(DELETE_PAYROLL_PERIOD)
    @use_args(payroll_period_args)
    def delete(self, args, payroll_period_id=None):
        payroll_period = PayrollPeriodModel.query.get(payroll_period_id)

        if payroll_period:
            payroll_period.delete_in_db()

            return marshal(payroll_period, payroll_period_fields)
        else:
            return {'message': 'Record not found.'}, 200
