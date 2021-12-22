from flask import request
from flask_restful import Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.v1.user.model import UserModel
from api.v1.client.model import ClientModel
from system_core.routine.tasks import execute
from system_core.report.generate_payroll_report import generate_payroll_report
import sys


class Employee(Resource):
    def get(self):
        client_id = request.args.get('client_id')
        payroll_period_id = request.args.get('payprd_id')
        routine_id = request.args.get('routine_id')
        client = ClientModel.query.get(client_id)
        
        if client:
            client_db = client.db_name
        else:
            return {
                'success': False,
                'message': 'Client not found'
            }, 401

        result = execute.apply_async(args=[routine_id, client_db, payroll_period_id])

        return {
            'task_id': result.id,
            'client_db': client_db,
            'payroll_period_id': payroll_period_id
        }

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        user = UserModel.find_by_username(current_user)

        client_id = request.form.get('compid')
        payroll_period_id = request.form.get('payprd_id')
        report_id = request.form.get('report_id')

        client = ClientModel.query.get(client_id)
        
        if client:
            client_db = client.db_name
        else:
            return {
                'success': False,
                'message': 'Client not found'
            }, 401

        data = {}
        data['client_db'] = client_db
        data['payroll_period_id'] = payroll_period_id
        data['report_id'] = report_id
        data['email'] = user.email

        generate_payroll_report(data)

        return {
            'success': True,
            'message': 'Report generated successfully and sent to email.'
        }, 200
