from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt_extended import (jwt_required, get_jwt_identity, get_raw_jwt)
from api.v1.permission.model import PermissionModel


permission_args = {
    'id': fields.Int(),
    'name': fields.Str()
}

permission_fields = {
    'id': mfields.Integer,
    'name': mfields.String
}

permission_list_fields = {
    'count': mfields.Integer,
    'permissions': mfields.List(mfields.Nested(permission_fields))
}


class Permission(Resource):
    @use_args(permission_args)
    def get(self, args, permission_id=None):
        if permission_id:
            permission = PermissionModel.query.filter_by(id=permission_id).first()

            return marshal(permission, permission_fields)
        else:
            permission = PermissionModel.query.all()

            return marshal({
                'count': len(permission),
                'permissions': [marshal(r, permission_fields) for r in permission]
            }, permission_list_fields)
        
    @use_args(permission_args)
    def post(self, args):
        permission = PermissionModel(**args)

        try:
            permission.save_to_db()

            return marshal(permission, permission_fields)
        except Exception as e:
            return {'message': 'Error: ' + str(e)}, 500

    @use_args(permission_args)
    def put(self, args, permission_id=None):
        permission = PermissionModel.query.get(permission_id)

        if permission:
            if 'name' in args:
                permission.name = args['name']
            
            permission.commit_to_db()

            return marshal(permission, permission_fields)
        else:
            return {'message': 'Record not found.'}, 200

    @use_args(permission_args)
    def delete(self, args, permission_id=None):
        permission = PermissionModel.query.get(permission_id)

        if permission:
            permission.delete_in_db()

            return marshal(permission, permission_fields)
        else:
            return {'message': 'Record not found.'}, 200
