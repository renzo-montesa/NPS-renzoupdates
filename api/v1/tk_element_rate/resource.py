from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.v1.user_role_permission_info.model import UserRolePermissionInfoModel, permission_required
from api.v1.tk_element_rate.model import TkElementRateModel


GET_TK_ELEMENT_RATE = 'get_tk_element_rate'
ADD_TK_ELEMENT_RATE = 'add_tk_element_rate'
EDIT_TK_ELEMENT_RATE = 'edit_tk_element_rate'
DELETE_TK_ELEMENT_RATE = 'delete_tk_element_rate'


tk_element_rate_args = {
    'id': fields.Int(),
    'branch_id': fields.Int(),
    'tk_element_id': fields.Int(),
    'percentage': fields.Float()
}

tk_element_rate_fields = {
    'id': mfields.Integer,
    'branch_id': mfields.Integer,
    'tk_element_id': mfields.Integer,
    'percentage': mfields.Float
}

tk_element_rate_list_fields = {
    'count': mfields.Integer,
    'tk_element_rates': mfields.List(mfields.Nested(tk_element_rate_fields))
}


class TkElementRate(Resource):
    @jwt_required
    @permission_required(GET_TK_ELEMENT_RATE)
    @use_args(tk_element_rate_args)
    def get(self, args, tk_element_rate_id=None):
        if tk_element_rate_id:
            tk_element_rate = TkElementRateModel.query.filter_by(id=tk_element_rate_id).first()

            return marshal(tk_element_rate, tk_element_rate_fields)

        else:
            tk_element_rates = TkElementRateModel.query.all()

            return marshal({
                'count': len(tk_element_rates),
                'tk_element_rates': [marshal(r, tk_element_rate_fields) for r in tk_element_rates]
            }, tk_element_rate_list_fields)
    
    @jwt_required
    @permission_required(ADD_TK_ELEMENT_RATE)
    @use_args(tk_element_rate_args)
    def post(self, args):
        tk_element_rate = TkElementRateModel(**args)

        try:
            tk_element_rate.save_to_db()

            return marshal(tk_element_rate, tk_element_rate_fields)
        except Exception as e:
            return {'message': 'Error: ' + str(e)}, 500

    @jwt_required
    @permission_required(EDIT_TK_ELEMENT_RATE)
    @use_args(tk_element_rate_args)
    def put(self, args, tk_element_rate_id=None):
        tk_element_rate = TkElementRateModel.query.get(tk_element_rate_id)

        if tk_element_rate:
            if 'branch_id' in args:
                tk_element_rate.field = args['branch_id']
            if 'tk_element_id' in args:
                tk_element_rate.tk_element_id = args['tk_element_id']
            if 'percentage' in args:
                tk_element_rate.percentage = args['percentage']
            
            tk_element_rate.commit_to_db()

            return marshal(tk_element_rate, tk_element_rate_fields)
        else:
            return {'message': 'Record not found.'}, 200

    @jwt_required
    @permission_required(DELETE_TK_ELEMENT_RATE)
    @use_args(tk_element_rate_args)
    def delete(self, args, tk_element_rate_id=None):
        tk_element_rate = TkElementRateModel.query.get(tk_element_rate_id)

        if tk_element_rate:
            tk_element_rate.delete_in_db()

            return marshal(tk_element_rate, tk_element_rate_fields)
        else:
            return {'message': 'Record not found.'}, 200
