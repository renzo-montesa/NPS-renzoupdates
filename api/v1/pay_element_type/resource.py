from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.v1.user_role_permission_info.model import UserRolePermissionInfoModel, permission_required
from api.v1.pay_element_type.model import PayElementTypeModel


GET_PAY_ELEMENT_TYPE = 'get_pay_element_type'
ADD_PAY_ELEMENT_TYPE = 'add_pay_element_type'
EDIT_PAY_ELEMENT_TYPE = 'edit_pay_element_type'
DELETE_PAY_ELEMENT_TYPE = 'delete_pay_element_type'


pay_element_type_args = {
    'id': fields.Int(),
    'code': fields.Str(),
    'description': fields.Str()
}

pay_element_type_fields = {
    'id': mfields.Integer,
    'code': mfields.String,
    'description': mfields.String
}

pay_element_type_list_fields = {
    'count': mfields.Integer,
    'pay_element_types': mfields.List(mfields.Nested(pay_element_type_fields))
}


class PayElementType(Resource):
    @jwt_required
    @permission_required(GET_PAY_ELEMENT_TYPE)
    @use_args(pay_element_type_args)
    def get(self, args, pay_element_type_id=None):
        if pay_element_type_id:
            pay_element_type = PayElementTypeModel.query.filter_by(id=pay_element_type_id).first()

            return marshal(pay_element_type, pay_element_type_fields)

        else:
            pay_element_types = PayElementTypeModel.query.all()

            return marshal({
                'count': len(pay_element_types),
                'pay_element_types': [marshal(r, pay_element_type_fields) for r in pay_element_types]
            }, pay_element_type_list_fields)
    
    @jwt_required
    @permission_required(ADD_PAY_ELEMENT_TYPE)
    @use_args(pay_element_type_args)
    def post(self, args):
        pay_element_type = PayElementTypeModel(**args)

        try:
            pay_element_type.save_to_db()

            return marshal(pay_element_type, pay_element_type_fields)
        except Exception as e:
            return {'message': 'Error: ' + str(e)}, 500

    @jwt_required
    @permission_required(EDIT_PAY_ELEMENT_TYPE)
    @use_args(pay_element_type_args)
    def put(self, args, pay_element_type_id=None):
        pay_element_type = PayElementTypeModel.query.get(pay_element_type_id)

        if pay_element_type:
            if 'code' in args:
                pay_element_type.code = args['code']
            if 'description' in args:
                pay_element_type.description = args['description']
            
            pay_element_type.commit_to_db()

            return marshal(pay_element_type, pay_element_type_fields)
        else:
            return {'message': 'Record not found.'}, 200

    @jwt_required
    @permission_required(DELETE_PAY_ELEMENT_TYPE)
    @use_args(pay_element_type_args)
    def delete(self, args, pay_element_type_id=None):
        pay_element_type = PayElementTypeModel.query.get(pay_element_type_id)

        if pay_element_type:
            pay_element_type.delete_in_db()

            return marshal(pay_element_type, pay_element_type_fields)
        else:
            return {'message': 'Record not found.'}, 200
