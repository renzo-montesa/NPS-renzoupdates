from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.v1.user_role_permission_info.model import UserRolePermissionInfoModel, permission_required
from api.v1.pay_element.model import PayElementModel


GET_PAY_ELEMENT = 'get_pay_element'
ADD_PAY_ELEMENT = 'add_pay_element'
EDIT_PAY_ELEMENT = 'edit_pay_element'
DELETE_PAY_ELEMENT = 'delete_pay_element'


pay_element_args = {
    'id': fields.Int(),
    'pay_element_type_id': fields.Int(),
    'code': fields.Str(),
    'description': fields.Str()
}

pay_element_fields = {
    'id': mfields.Integer,
    'pay_element_type_id': mfields.Integer,
    'code': mfields.String,
    'description': mfields.String
}

pay_element_list_fields = {
    'count': mfields.Integer,
    'pay_elements': mfields.List(mfields.Nested(pay_element_fields))
}


class PayElement(Resource):
    @jwt_required
    @permission_required(GET_PAY_ELEMENT)
    @use_args(pay_element_args)
    def get(self, args, pay_element_id=None):
        if pay_element_id:
            pay_element = PayElementModel.query.filter_by(id=pay_element_id).first()

            return marshal(pay_element, pay_element_fields)

        else:
            pay_elements = PayElementModel.query.all()

            return marshal({
                'count': len(pay_elements),
                'pay_elements': [marshal(r, pay_element_fields) for r in pay_elements]
            }, pay_element_list_fields)
    
    @jwt_required
    @permission_required(ADD_PAY_ELEMENT)
    @use_args(pay_element_args)
    def post(self, args):
        pay_element = PayElementModel(**args)

        try:
            pay_element.save_to_db()

            return marshal(pay_element, pay_element_fields)
        except Exception as e:
            return {'message': 'Error: ' + str(e)}, 500

    @jwt_required
    @permission_required(EDIT_PAY_ELEMENT)
    @use_args(pay_element_args)
    def put(self, args, pay_element_id=None):
        pay_element = PayElementModel.query.get(pay_element_id)

        if pay_element:
            if 'pay_element_type_id' in args:
                pay_element.pay_element_type_id = args['pay_element_type_id']
            if 'code' in args:
                pay_element.code = args['code']
            if 'description' in args:
                pay_element.description = args['description']
            
            pay_element.commit_to_db()

            return marshal(pay_element, pay_element_fields)
        else:
            return {'message': 'Record not found.'}, 200

    @jwt_required
    @permission_required(DELETE_PAY_ELEMENT)
    @use_args(pay_element_args)
    def delete(self, args, pay_element_id=None):
        pay_element = PayElementModel.query.get(pay_element_id)

        if pay_element:
            pay_element.delete_in_db()

            return marshal(pay_element, pay_element_fields)
        else:
            return {'message': 'Record not found.'}, 200
