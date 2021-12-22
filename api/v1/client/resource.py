from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from webargs.flaskparser import use_args
from api.v1.client.model import ClientModel
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.v1.user_role_permission_info.model import UserRolePermissionInfoModel, permission_required
from api.v1.user_branch_client_info.model import UserBranchClientInfoModel


GET_CLIENT = 'get_client'
ADD_CLIENT = 'add_client'
EDIT_CLIENT = 'edit_client'
DELETE_CLIENT = 'delete_client'


client_args = {
    'id': fields.Int(),
    'name': fields.Str(),
    'db_name': fields.Str()
}

client_fields = {
    'id': mfields.Integer,
    'name': mfields.String,
    'db_name': mfields.String
}

client_list_fields = {
    'count': mfields.Integer,
    'clients': mfields.List(mfields.Nested(client_fields))
}


class Client(Resource):
    @jwt_required
    @permission_required(GET_CLIENT)
    @use_args(client_args)
    def get(self, args, client_id=None):
        current_user = get_jwt_identity()

        if client_id:
            user_client_access = UserBranchClientInfoModel.has_user_client_access(current_user, client_id)

            if (not user_client_access):
                return {'message': 'Unauthorized access'}, 403

            client = ClientModel.query.filter_by(id=client_id).first()

            return marshal(client, client_fields)
        else:
            clients = UserBranchClientInfoModel.get_clients_by_username(current_user)['result']

            return marshal({
                'count': len(clients),
                'clients': [marshal(r, client_fields) for r in clients]
            }, client_list_fields)
    
    @jwt_required
    @permission_required(ADD_CLIENT)
    @use_args(client_args)
    def post(self, args):
        client = ClientModel(**args)

        try:
            client.save_to_db()

            return marshal(client, client_fields)
        except Exception as e:
            return {'message': 'Error: ' + str(e)}, 500

    @jwt_required
    @permission_required(EDIT_CLIENT)
    @use_args(client_args)
    def put(self, args, client_id=None):
        current_user = get_jwt_identity()
        client = ClientModel.query.get(client_id)

        if client:
            user_client_access = UserBranchClientInfoModel.has_user_client_access(current_user, client_id)

            if (not user_client_access):
                return {'message': 'Unauthorized access'}, 403

            if 'name' in args:
                client.name = args['name']
            
            client.commit_to_db()

            return marshal(client, client_fields)
        else:
            return {'message': 'Record not found.'}, 200

    @jwt_required
    @permission_required(DELETE_CLIENT)
    @use_args(client_args)
    def delete(self, args, client_id=None):
        current_user = get_jwt_identity()
        client = ClientModel.query.get(client_id)

        if client:
            user_client_access = UserBranchClientInfoModel.has_user_client_access(current_user, client_id)

            if (not user_client_access):
                return {'message': 'Unauthorized access'}, 403
                
            client.delete_in_db()

            return marshal(client, client_fields)
        else:
            return {'message': 'Record not found.'}, 200
