from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.v1.role.model import RoleModel
from api.v1.user_role_permission_info.model import UserRolePermissionInfoModel, permission_required


GET_ROLE = 'get_role'
ADD_ROLE = 'add_role'
EDIT_ROLE = 'edit_role'
DELETE_ROLE = 'delete_role'


role_args = {
    'id': fields.Int(),
    'name': fields.Str()
}

role_fields = {
    'id': mfields.Integer,
    'name': mfields.String
}

role_list_fields = {
    'count': mfields.Integer,
    'roles': mfields.List(mfields.Nested(role_fields))
}


class Role(Resource):
    @jwt_required
    @permission_required(GET_ROLE)
    @use_args(role_args)
    def get(self, args, role_id=None):
        if role_id:
            role = RoleModel.query.filter_by(id=role_id).first()

            return marshal(role, role_fields)
        else:
            role = RoleModel.query.all()

            return marshal({
                'count': len(role),
                'roles': [marshal(r, role_fields) for r in role]
            }, role_list_fields)
        
    @jwt_required
    @permission_required(ADD_ROLE)
    @use_args(role_args)
    def post(self, args):
        role = RoleModel(**args)

        try:
            role.save_to_db()

            return marshal(role, role_fields)
        except Exception as e:
            return {'message': 'Error: ' + str(e)}, 500

    @jwt_required
    @permission_required(EDIT_ROLE)
    @use_args(role_args)
    def put(self, args, role_id=None):
        role = RoleModel.query.get(role_id)

        if role:
            if 'name' in args:
                role.name = args['name']
            
            role.commit_to_db()

            return marshal(role, role_fields)
        else:
            return {'message': 'Record not found.'}, 200

    @jwt_required
    @permission_required(DELETE_ROLE)
    @use_args(role_args)
    def delete(self, args, role_id=None):
        role = RoleModel.query.get(role_id)

        if role:
            role.delete_in_db()

            return marshal(role, role_fields)
        else:
            return {'message': 'Record not found.'}, 200
