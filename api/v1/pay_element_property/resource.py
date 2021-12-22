from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.v1.user_role_permission_info.model import UserRolePermissionInfoModel, permission_required
from api.v1.pay_element_property.model import PayElementPropertyModel


GET_PAY_ELEMENT_PROPERTY = 'get_pay_element_property'
ADD_PAY_ELEMENT_PROPERTY = 'add_pay_element_property'
EDIT_PAY_ELEMENT_PROPERTY = 'edit_pay_element_property'
DELETE_PAY_ELEMENT_PROPERTY = 'delete_pay_element_property'


pay_element_property_args = {
    'id': fields.Int(),
    'field': fields.Str(),
    'description': fields.Str(),
    'is_required': fields.Bool()
}

pay_element_property_fields = {
    'id': mfields.Integer,
    'field': mfields.String,
    'description': mfields.String,
    'is_required': mfields.Boolean
}

pay_element_property_list_fields = {
    'count': mfields.Integer,
    'pay_element_properties': mfields.List(mfields.Nested(pay_element_property_fields))
}


class PayElementProperty(Resource):
    @jwt_required
    @permission_required(GET_PAY_ELEMENT_PROPERTY)
    @use_args(pay_element_property_args)
    def get(self, args, pay_element_property_id=None):
        if pay_element_property_id:
            pay_element_property = PayElementPropertyModel.query.filter_by(id=pay_element_property_id).first()

            return marshal(pay_element_property, pay_element_property_fields)

        else:
            pay_element_properties = PayElementPropertyModel.query.all()

            return marshal({
                'count': len(pay_element_properties),
                'pay_element_properties': [marshal(r, pay_element_property_fields) for r in pay_element_properties]
            }, pay_element_property_list_fields)
    
    @jwt_required
    @permission_required(ADD_PAY_ELEMENT_PROPERTY)
    @use_args(pay_element_property_args)
    def post(self, args):
        pay_element_property = PayElementPropertyModel(**args)

        try:
            pay_element_property.save_to_db()

            return marshal(pay_element_property, pay_element_property_fields)
        except Exception as e:
            return {'message': 'Error: ' + str(e)}, 500

    @jwt_required
    @permission_required(EDIT_PAY_ELEMENT_PROPERTY)
    @use_args(pay_element_property_args)
    def put(self, args, pay_element_property_id=None):
        pay_element_property = PayElementPropertyModel.query.get(pay_element_property_id)

        if pay_element_property:
            if 'field' in args:
                pay_element_property.field = args['field']
            if 'description' in args:
                pay_element_property.description = args['description']
            if 'is_required' in args:
                pay_element_property.is_required = args['is_required']
            
            pay_element_property.commit_to_db()

            return marshal(pay_element_property, pay_element_property_fields)
        else:
            return {'message': 'Record not found.'}, 200

    @jwt_required
    @permission_required(DELETE_PAY_ELEMENT_PROPERTY)
    @use_args(pay_element_property_args)
    def delete(self, args, pay_element_property_id=None):
        pay_element_property = PayElementPropertyModel.query.get(pay_element_property_id)

        if pay_element_property:
            pay_element_property.delete_in_db()

            return marshal(pay_element_property, pay_element_property_fields)
        else:
            return {'message': 'Record not found.'}, 200
