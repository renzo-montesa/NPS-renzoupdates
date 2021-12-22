from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from webargs.flaskparser import use_args
from api.v1.activity_log.model import ActivityLogModel


activity_log_args = {
    'id': fields.Int(),
    'name': fields.Str()
}

activity_log_fields = {
    'id': mfields.Integer,
    'name': mfields.String
}

activity_log_list_fields = {
    'count': mfields.Integer,
    'activity_logs': mfields.List(mfields.Nested(activity_log_fields))
}


class ActivityLog(Resource):
    @use_args(activity_log_args)
    def get(self, args, activity_log_id=None):
        if activity_log_id:
            activity_log = ActivityLogModel.query.filter_by(id=activity_log_id).first()

            return marshal(activity_log, activity_log_fields)
        else:
            activity_log = ActivityLogModel.query.all()

            return marshal({
                'count': len(activity_log),
                'activity_logs': [marshal(r, activity_log_fields) for r in activity_log]
            }, activity_log_list_fields)
    
    @use_args(activity_log_args)
    def post(self, args):
        activity_log = ActivityLogModel(**args)

        try:
            activity_log.save_to_db()

            return marshal(activity_log, activity_log_fields)
        except Exception as e:
            return {'message': 'Error: ' + str(e)}, 500

    @use_args(activity_log_args)
    def put(self, args, activity_log_id=None):
        activity_log = ActivityLogModel.query.get(activity_log_id)

        if activity_log:
            if 'name' in args:
                activity_log.name = args['name']
            
            activity_log.commit_to_db()

            return marshal(activity_log, activity_log_fields)
        else:
            return {'message': 'Record not found.'}, 200

    @use_args(activity_log_args)
    def delete(self, args, activity_log_id=None):
        activity_log = ActivityLogModel.query.get(activity_log_id)

        if activity_log:
            activity_log.delete_in_db()

            return marshal(activity_log, activity_log_fields)
        else:
            return {'message': 'Record not found.'}, 200
