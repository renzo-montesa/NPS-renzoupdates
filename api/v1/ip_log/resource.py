from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.v1.user_role_permission_info.model import UserRolePermissionInfoModel, permission_required
from api.v1.ip_log.model import IpLogModel


GET_IP_LOG = 'get_ip_log'
ADD_IP_LOG = 'add_ip_log'
EDIT_IP_LOG = 'edit_ip_log'
DELETE_IP_LOG = 'delete_ip_log'


ip_log_args = {
    'id': fields.Int(),
    'ip_address': fields.Str(),
    'country': fields.Str(),
    'region': fields.Str(),
    'city': fields.Str(),
    'zip': fields.Str(),
    'latitude': fields.Float(),
    'longitude': fields.Float()
}

ip_log_fields = {
    'id': mfields.Integer,
    'ip_address': mfields.String,
    'country': mfields.String,
    'region': mfields.String,
    'city': mfields.String,
    'zip': mfields.String,
    'latitude': mfields.Float,
    'longitude': mfields.Float
}

ip_log_list_fields = {
    'count': mfields.Integer,
    'ip_logs': mfields.List(mfields.Nested(ip_log_fields))
}


class IpLog(Resource):
    @jwt_required
    @permission_required(GET_IP_LOG)
    @use_args(ip_log_args)
    def get(self, args, ip_log_id=None):
        if ip_log_id:
            ip_log = IpLogModel.query.filter_by(id=ip_log_id).first()

            return marshal(ip_log, ip_log_fields)

        else:
            ip_logs = IpLogModel.query.all()

            return marshal({
                'count': len(ip_logs),
                'ip_logs': [marshal(r, ip_log_fields) for r in ip_logs]
            }, ip_log_list_fields)
    
    @jwt_required
    @permission_required(ADD_IP_LOG)
    @use_args(ip_log_args)
    def post(self, args):
        ip_log = IpLogModel(**args)

        try:
            ip_log.save_to_db()

            return marshal(ip_log, ip_log_fields)
        except Exception as e:
            return {'message': 'Error: ' + str(e)}, 500

    @jwt_required
    @permission_required(EDIT_IP_LOG)
    @use_args(ip_log_args)
    def put(self, args, ip_log_id=None):
        ip_log = IpLogModel.query.get(ip_log_id)

        if ip_log:
            if 'ip_address' in args:
                ip_log.ip_address = args['ip_address']
            if 'country' in args:
                ip_log.country = args['country']
            if 'region' in args:
                ip_log.region = args['region']
            if 'city' in args:
                ip_log.city = args['city']
            if 'zip' in args:
                ip_log.zip = args['zip']
            if 'latitude' in args:
                ip_log.latitude = args['latitude']
            if 'longitude' in args:
                ip_log.longitude = args['longitude']
            
            ip_log.commit_to_db()

            return marshal(ip_log, ip_log_fields)
        else:
            return {'message': 'Record not found.'}, 200

    @jwt_required
    @permission_required(DELETE_IP_LOG)
    @use_args(ip_log_args)
    def delete(self, args, ip_log_id=None):
        ip_log = IpLogModel.query.get(ip_log_id)

        if ip_log:
            ip_log.delete_in_db()

            return marshal(ip_log, ip_log_fields)
        else:
            return {'message': 'Record not found.'}, 200
