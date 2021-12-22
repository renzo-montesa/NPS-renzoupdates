from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.v1.user_role_permission_info.model import UserRolePermissionInfoModel, permission_required
from api.v1.tk_element_type.model import TkElementTypeModel


GET_TK_ELEMENT_TYPE = 'get_tk_element_type'
ADD_TK_ELEMENT_TYPE = 'add_tk_element_type'
EDIT_TK_ELEMENT_TYPE = 'edit_tk_element_type'
DELETE_TK_ELEMENT_TYPE = 'delete_tk_element_type'


tk_element_type_args = {
    'id': fields.Int(),
    'code': fields.Str(),
    'description': fields.Str()
}

tk_element_type_fields = {
    'id': mfields.Integer,
    'code': mfields.String,
    'description': mfields.String
}

tk_element_type_list_fields = {
    'count': mfields.Integer,
    'tk_element_types': mfields.List(mfields.Nested(tk_element_type_fields))
}


class TkElementType(Resource):
    @jwt_required
    @permission_required(GET_TK_ELEMENT_TYPE)
    @use_args(tk_element_type_args)
    def get(self, args, tk_element_type_id=None):
        if tk_element_type_id:
            tk_element_type = TkElementTypeModel.query.filter_by(id=tk_element_type_id).first()

            return marshal(tk_element_type, tk_element_type_fields)

        else:
            tk_element_types = TkElementTypeModel.query.all()

            return marshal({
                'count': len(tk_element_types),
                'tk_element_types': [marshal(r, tk_element_type_fields) for r in tk_element_types]
            }, tk_element_type_list_fields)
    
    @jwt_required
    @permission_required(ADD_TK_ELEMENT_TYPE)
    @use_args(tk_element_type_args)
    def post(self, args):
        tk_element_type = TkElementTypeModel(**args)

        try:
            tk_element_type.save_to_db()

            return marshal(tk_element_type, tk_element_type_fields)
        except Exception as e:
            return {'message': 'Error: ' + str(e)}, 500

    @jwt_required
    @permission_required(EDIT_TK_ELEMENT_TYPE)
    @use_args(tk_element_type_args)
    def put(self, args, tk_element_type_id=None):
        tk_element_type = TkElementTypeModel.query.get(tk_element_type_id)

        if tk_element_type:
            if 'code' in args:
                tk_element_type.code = args['code']
            if 'description' in args:
                tk_element_type.description = args['description']
            
            tk_element_type.commit_to_db()

            return marshal(tk_element_type, tk_element_type_fields)
        else:
            return {'message': 'Record not found.'}, 200

    @jwt_required
    @permission_required(DELETE_TK_ELEMENT_TYPE)
    @use_args(tk_element_type_args)
    def delete(self, args, tk_element_type_id=None):
        tk_element_type = TkElementTypeModel.query.get(tk_element_type_id)

        if tk_element_type:
            tk_element_type.delete_in_db()

            return marshal(tk_element_type, tk_element_type_fields)
        else:
            return {'message': 'Record not found.'}, 200
