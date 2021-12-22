from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.v1.user_role_permission_info.model import UserRolePermissionInfoModel, permission_required
from api.v1.tk_element.model import TkElementModel


GET_TK_ELEMENT = 'get_tk_element'
ADD_TK_ELEMENT = 'add_tk_element'
EDIT_TK_ELEMENT = 'edit_tk_element'
DELETE_TK_ELEMENT = 'delete_tk_element'


tk_element_args = {
    'id': fields.Int(),
    'pay_element_id': fields.Int(),
    'tk_element_type_id': fields.Int(),
    'code': fields.Str(),
    'description': fields.Str()
}

tk_element_fields = {
    'id': mfields.Integer,
    'pay_element_id': mfields.Integer,
    'tk_element_type_id': mfields.Integer,
    'code': mfields.String,
    'description': mfields.String
}

tk_element_list_fields = {
    'count': mfields.Integer,
    'tk_elements': mfields.List(mfields.Nested(tk_element_fields))
}


class TkElement(Resource):
    @jwt_required
    @permission_required(GET_TK_ELEMENT)
    @use_args(tk_element_args)
    def get(self, args, tk_element_id=None):
        if tk_element_id:
            tk_element = TkElementModel.query.filter_by(id=tk_element_id).first()

            return marshal(tk_element, tk_element_fields)

        else:
            tk_elements = TkElementModel.query.all()

            return marshal({
                'count': len(tk_elements),
                'tk_elements': [marshal(r, tk_element_fields) for r in tk_elements]
            }, tk_element_list_fields)
    
    @jwt_required
    @permission_required(ADD_TK_ELEMENT)
    @use_args(tk_element_args)
    def post(self, args):
        tk_element = TkElementModel(**args)

        try:
            tk_element.save_to_db()

            return marshal(tk_element, tk_element_fields)
        except Exception as e:
            return {'message': 'Error: ' + str(e)}, 500

    @jwt_required
    @permission_required(EDIT_TK_ELEMENT)
    @use_args(tk_element_args)
    def put(self, args, tk_element_id=None):
        tk_element = TkElementModel.query.get(tk_element_id)

        if tk_element:
            if 'pay_element_id' in args:
                tk_element.pay_element_id = args['pay_element_id']
            if 'tk_element_type_id' in args:
                tk_element.tk_element_type_id = args['tk_element_type_id']
            if 'code' in args:
                tk_element.code = args['code']
            if 'description' in args:
                tk_element.description = args['description']
            
            tk_element.commit_to_db()

            return marshal(tk_element, tk_element_fields)
        else:
            return {'message': 'Record not found.'}, 200

    @jwt_required
    @permission_required(DELETE_TK_ELEMENT)
    @use_args(tk_element_args)
    def delete(self, args, tk_element_id=None):
        tk_element = TkElementModel.query.get(tk_element_id)

        if tk_element:
            tk_element.delete_in_db()

            return marshal(tk_element, tk_element_fields)
        else:
            return {'message': 'Record not found.'}, 200
