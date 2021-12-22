from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from api.v1.client.model import ClientModel
from api.v1.user_role_permission_info.model import UserRolePermissionInfoModel, permission_required
from api.v1.user_branch_client_info.model import UserBranchClientInfoModel
from api.v1.employee.model import EmployeeModel


GET_MULTI_TENANCY = 'get_multi_tenancy'
ADD_MULTI_TENANCY = 'add_multi_tenancy'
EDIT_MULTI_TENANCY = 'edit_multi_tenancy'
DELETE_MULTI_TENANCY = 'delete_multi_tenancy'


client_fields = {
    'id': mfields.Integer,
    'name': mfields.String,
    'db_name': mfields.String
}

client_list_fields = {
    'count': mfields.Integer,
    'clients': mfields.List(mfields.Nested(client_fields))
}


class MultiTenancy(Resource):
    def get(self, db_name=None):
        if db_name:
            employees = EmployeeModel.get_all_employees(db_name)

            return {
                'employees': employees
            }
        else:
            clients = ClientModel.get_all()['clients']

            return marshal({
                'clients': clients
            }, client_list_fields)
