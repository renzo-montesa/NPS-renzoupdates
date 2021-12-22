from flask import request
from sqlalchemy.sql.expression import update
from flask_restful import Resource
from flask_jwt_extended import (jwt_required)
from api.v1.user_role_permission_info.model import permission_required
from api.v1.client.model import ClientModel
from api.v1.payroll_period.model import PayrollPeriodModel
from api.v1.payslip.model import PayslipModel


POST_FINALIZE = 'post_finalize'


class Finalize(Resource):
    def post(self):
        client_id = request.form.get('compid')
        payroll_period_id = request.form.get('payprd_id')

        client = ClientModel.query.get(client_id)
        if client:
            client_db = client.db_name
        else:
            return {
                'success': False,
                'message': 'Error encountered. Client not found.'
            }, 200

        payroll_period, pps = PayrollPeriodModel.get_obj_by_filter(client_db, id=payroll_period_id)
        if not payroll_period:
            return {
                'success': False,
                'message': 'Error encountered. Payroll period not found.'
            }, 200

        PayslipModel.finalizeByFilter(client_db, payroll_period_id=payroll_period_id)
        
        payroll_period.is_summarized = 1
        payroll_period.is_locked = 1
        pps.commit()

        return {
            'success': True,
            'message': 'Payroll is now finalized and locked.'
        }, 200
