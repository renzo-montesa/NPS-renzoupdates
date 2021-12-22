from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.v1.user_role_permission_info.model import permission_required
from api.v1.upload_file.model import UploadFileModel


GET_UPLOAD_FILE = 'get_upload_file'
ADD_UPLOAD_FILE = 'add_upload_file'
EDIT_UPLOAD_FILE = 'edit_upload_file'
DELETE_UPLOAD_FILE = 'delete_upload_file'


upload_file_args = {
    'id': fields.Int(),
    'file_uid': fields.Str(),
    'fullpath': fields.Str(),
    'filename': fields.Str()
}

upload_file_fields = {
    'id': mfields.Integer,
    'file_uid': mfields.String,
    'fullpath': mfields.String,
    'filename': mfields.String
}

upload_file_list_fields = {
    'count': mfields.Integer,
    'upload_files': mfields.List(mfields.Nested(upload_file_fields))
}


class UploadFile(Resource):
    @jwt_required
    @permission_required(GET_UPLOAD_FILE)
    @use_args(upload_file_args)
    def get(self, args, upload_file_id=None):
        if upload_file_id:
            upload_file = UploadFileModel.query.filter_by(id=upload_file_id).first()

            return marshal(upload_file, upload_file_fields)

        else:
            upload_files = UploadFileModel.query.all()

            return marshal({
                'count': len(upload_files),
                'upload_files': [marshal(r, upload_file_fields) for r in upload_files]
            }, upload_file_list_fields)
    
    @jwt_required
    @permission_required(ADD_UPLOAD_FILE)
    @use_args(upload_file_args)
    def post(self, args):
        upload_file = UploadFileModel(**args)

        try:
            upload_file.save_to_db()

            return marshal(upload_file, upload_file_fields)
        except Exception as e:
            return {'message': 'Error: ' + str(e)}, 500

    @jwt_required
    @permission_required(EDIT_UPLOAD_FILE)
    @use_args(upload_file_args)
    def put(self, args, upload_file_id=None):
        upload_file = UploadFileModel.query.get(upload_file_id)

        if upload_file:
            if 'file_uid' in args:
                upload_file.file_uid = args['file_uid']
            if 'fullpath' in args:
                upload_file.fullpath = args['fullpath']
            if 'filename' in args:
                upload_file.filename = args['filename']
            
            upload_file.commit_to_db()

            return marshal(upload_file, upload_file_fields)
        else:
            return {'message': 'Record not found.'}, 200

    @jwt_required
    @permission_required(DELETE_UPLOAD_FILE)
    @use_args(upload_file_args)
    def delete(self, args, upload_file_id=None):
        upload_file = UploadFileModel.query.get(upload_file_id)

        if upload_file:
            upload_file.delete_in_db()

            return marshal(upload_file, upload_file_fields)
        else:
            return {'message': 'Record not found.'}, 200
