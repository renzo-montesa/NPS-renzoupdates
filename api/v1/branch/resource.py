from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from webargs.flaskparser import use_args
from api.v1.branch.model import BranchModel
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.v1.user_role_permission_info.model import UserRolePermissionInfoModel, permission_required
from api.v1.user_branch_info.model import UserBranchInfoModel


GET_BRANCH = 'get_branch'
ADD_BRANCH = 'add_branch'
EDIT_BRANCH = 'edit_branch'
DELETE_BRANCH = 'delete_branch'


branch_args = {
    'id': fields.Int(),
    'client_id': fields.Int(),
    'name': fields.Str(),
    'address': fields.Str()
}

branch_fields = {
    'id': mfields.Integer,
    'client_id': mfields.Integer,
    'name': mfields.String,
    'address': mfields.String
}

branch_list_fields = {
    'count': mfields.Integer,
    'branches': mfields.List(mfields.Nested(branch_fields))
}


class Branch(Resource):
    @jwt_required
    @permission_required(GET_BRANCH)
    @use_args(branch_args)
    def get(self, args, branch_id=None):
        current_user = get_jwt_identity()

        if 'client_id' in args:
            branches = UserBranchInfoModel.get_branches_by_username_and_client(current_user, args['client_id'])['result']
            
            return marshal({
                'count': len(branches),
                'branches': [marshal(r, branch_fields) for r in branches]
            }, branch_list_fields)

        elif branch_id:
            user_branch_access = UserBranchInfoModel.has_user_branch_access(current_user, branch_id)

            if (not user_branch_access):
                return {'message': 'Unauthorized access'}, 403

            branch = BranchModel.query.filter_by(id=branch_id).first()

            return marshal(branch, branch_fields)

        else:
            branches = UserBranchInfoModel.get_branches_by_username(current_user)['result']

            return marshal({
                'count': len(branches),
                'branches': [marshal(r, branch_fields) for r in branches]
            }, branch_list_fields)
    
    @jwt_required
    @permission_required(ADD_BRANCH)
    @use_args(branch_args)
    def post(self, args):
        branch = BranchModel(**args)

        try:
            branch.save_to_db()

            return marshal(branch, branch_fields)
        except Exception as e:
            return {'message': 'Error: ' + str(e)}, 500

    @jwt_required
    @permission_required(EDIT_BRANCH)
    @use_args(branch_args)
    def put(self, args, branch_id=None):
        current_user = get_jwt_identity()
        branch = BranchModel.query.get(branch_id)

        if branch:
            user_branch_access = UserBranchInfoModel.has_user_branch_access(current_user, branch_id)

            if (not user_branch_access):
                return {'message': 'Unauthorized access'}, 403

            if 'client_id' in args:
                branch.client_id = args['client_id']
            if 'name' in args:
                branch.name = args['name']
            if 'address' in args:
                branch.address = args['address']
            
            branch.commit_to_db()

            return marshal(branch, branch_fields)
        else:
            return {'message': 'Record not found.'}, 200

    @jwt_required
    @permission_required(DELETE_BRANCH)
    @use_args(branch_args)
    def delete(self, args, branch_id=None):
        current_user = get_jwt_identity()
        branch = BranchModel.query.get(branch_id)

        if branch:
            user_branch_access = UserBranchInfoModel.has_user_branch_access(current_user, branch_id)

            if (not user_branch_access):
                return {'message': 'Unauthorized access'}, 403

            branch.delete_in_db()

            return marshal(branch, branch_fields)
        else:
            return {'message': 'Record not found.'}, 200
