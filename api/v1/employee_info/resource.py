from flask import request
from flask_restful import Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from webargs import fields
from webargs.flaskparser import use_args
from api.v1.client.model import ClientModel
from api.v1.employee.model import EmployeeModel
from api.v1.user_role_permission_info.model import permission_required
import sys


GET_EMPLOYEE_INFO = 'get_employee_info'


get_args = {
    'client_id': fields.Int()
}


class EmployeeInfo(Resource):
    @jwt_required
    @use_args(get_args)
    def get(self, args):
        if 'client_id' in args:
            client_id = args['client_id']
            print('Client id: ' + str(client_id), file=sys.stderr)

            client = ClientModel.query.get(client_id)
            if client:
                print('Client found', file=sys.stderr)
                client_db = client.db_name
            else:
                print('Client not found', file=sys.stderr)
                return [], 200

            return EmployeeModel.get_all_basic_infos(client_db)
        else:
            return [], 200
