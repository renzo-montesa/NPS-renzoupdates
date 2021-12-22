from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.v1.user_role_permission_info.model import UserRolePermissionInfoModel, permission_required
from api.v1.pay_element_property_value.model import PayElementPropertyValueModel


GET_PAY_ELEMENT_PROPERTY_VALUE = 'get_pay_element_property_value'
ADD_PAY_ELEMENT_PROPERTY_VALUE = 'add_pay_element_property_value'
EDIT_PAY_ELEMENT_PROPERTY_VALUE = 'edit_pay_element_property_value'
DELETE_PAY_ELEMENT_PROPERTY_VALUE = 'delete_pay_element_property_value'


pay_element_property_value_args = {
    'id': fields.Int(),
    'pay_element_id': fields.Int(),
    'pay_element_property_id': fields.Int(),
    'value': fields.Str()
}

pay_element_property_value_fields = {
    'id': mfields.Integer,
    'pay_element_id': mfields.Integer,
    'pay_element_property_id': mfields.Integer,
    'value': mfields.String
}

pay_element_property_value_list_fields = {
    'count': mfields.Integer,
    'pay_element_property_values': mfields.List(mfields.Nested(pay_element_property_value_fields))
}


class PayElementPropertyValue(Resource):
    @jwt_required
    @permission_required(GET_PAY_ELEMENT_PROPERTY_VALUE)
    @use_args(pay_element_property_value_args)
    def get(self, args, pay_element_property_value_id=None):
        if pay_element_property_value_id:
            pay_element_property_value = PayElementPropertyValueModel.query.filter_by(id=pay_element_property_value_id).first()

            return marshal(pay_element_property_value, pay_element_property_value_fields)

        else:
            pay_element_property_values = PayElementPropertyValueModel.query.all()

            return marshal({
                'count': len(pay_element_property_values),
                'pay_element_property_values': [marshal(r, pay_element_property_value_fields) for r in pay_element_property_values]
            }, pay_element_property_value_list_fields)
    
    @jwt_required
    @permission_required(ADD_PAY_ELEMENT_PROPERTY_VALUE)
    @use_args(pay_element_property_value_args)
    def post(self, args):
        pay_element_property_value = PayElementPropertyValueModel(**args)

        try:
            pay_element_property_value.save_to_db()

            return marshal(pay_element_property_value, pay_element_property_value_fields)
        except Exception as e:
            return {'message': 'Error: ' + str(e)}, 500

    @jwt_required
    @permission_required(EDIT_PAY_ELEMENT_PROPERTY_VALUE)
    @use_args(pay_element_property_value_args)
    def put(self, args, pay_element_property_value_id=None):
        pay_element_property_value = PayElementPropertyValueModel.query.get(pay_element_property_value_id)

        if pay_element_property_value:
            if 'pay_element_id' in args:
                pay_element_property_value.field = args['pay_element_id']
            if 'pay_element_property_id' in args:
                pay_element_property_value.pay_element_property_id = args['pay_element_property_id']
            if 'value' in args:
                pay_element_property_value.value = args['value']
            
            pay_element_property_value.commit_to_db()

            return marshal(pay_element_property_value, pay_element_property_value_fields)
        else:
            return {'message': 'Record not found.'}, 200

    @jwt_required
    @permission_required(DELETE_PAY_ELEMENT_PROPERTY_VALUE)
    @use_args(pay_element_property_value_args)
    def delete(self, args, pay_element_property_value_id=None):
        pay_element_property_value = PayElementPropertyValueModel.query.get(pay_element_property_value_id)

        if pay_element_property_value:
            pay_element_property_value.delete_in_db()

            return marshal(pay_element_property_value, pay_element_property_value_fields)
        else:
            return {'message': 'Record not found.'}, 200
