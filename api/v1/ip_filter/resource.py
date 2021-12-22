from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.v1.user_role_permission_info.model import UserRolePermissionInfoModel, permission_required
from api.v1.ip_filter.model import IpFilterModel


GET_IP_FILTER = 'get_ip_filter'
ADD_IP_FILTER = 'add_ip_filter'
EDIT_IP_FILTER = 'edit_ip_filter'
DELETE_IP_FILTER = 'delete_ip_filter'


ip_filter_args = {
    'id': fields.Int(),
    'ip_address': fields.Str(),
    'is_allowed': fields.Bool()
}

ip_filter_fields = {
    'id': mfields.Integer,
    'ip_address': mfields.String,
    'is_allowed': mfields.Boolean
}

ip_filter_list_fields = {
    'count': mfields.Integer,
    'ip_filters': mfields.List(mfields.Nested(ip_filter_fields))
}


class IpFilter(Resource):
    @jwt_required
    @permission_required(GET_IP_FILTER)
    @use_args(ip_filter_args)
    def get(self, args, ip_filter_id=None):
        if ip_filter_id:
            ip_filter = IpFilterModel.query.filter_by(id=ip_filter_id).first()

            return marshal(ip_filter, ip_filter_fields)

        else:
            ip_filters = IpFilterModel.query.all()

            return marshal({
                'count': len(ip_filters),
                'ip_filters': [marshal(r, ip_filter_fields) for r in ip_filters]
            }, ip_filter_list_fields)
    
    @jwt_required
    @permission_required(ADD_IP_FILTER)
    @use_args(ip_filter_args)
    def post(self, args):
        ip_filter = IpFilterModel(**args)

        try:
            ip_filter.save_to_db()

            return marshal(ip_filter, ip_filter_fields)
        except Exception as e:
            return {'message': 'Error: ' + str(e)}, 500

    @jwt_required
    @permission_required(EDIT_IP_FILTER)
    @use_args(ip_filter_args)
    def put(self, args, ip_filter_id=None):
        ip_filter = IpFilterModel.query.get(ip_filter_id)

        if ip_filter:
            if 'ip_address' in args:
                ip_filter.ip_address = args['ip_address']
            if 'is_allowed' in args:
                ip_filter.is_allowed = args['is_allowed']
            
            ip_filter.commit_to_db()

            return marshal(ip_filter, ip_filter_fields)
        else:
            return {'message': 'Record not found.'}, 200

    @jwt_required
    @permission_required(DELETE_IP_FILTER)
    @use_args(ip_filter_args)
    def delete(self, args, ip_filter_id=None):
        ip_filter = IpFilterModel.query.get(ip_filter_id)

        if ip_filter:
            ip_filter.delete_in_db()

            return marshal(ip_filter, ip_filter_fields)
        else:
            return {'message': 'Record not found.'}, 200
