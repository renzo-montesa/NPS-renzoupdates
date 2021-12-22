from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, get_jti, decode_token
from api.v1.user.model import UserModel
from api.v1.token.model import WhitelistedTokenModel
from api.v1.activity_log.model import ActivityLogModel
from api.v1.ip_filter.model import (ip_has_access)
from datetime import datetime


parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)


class UserRegistration(Resource):
    @ip_has_access
    def post(self):
        data = parser.parse_args()

        activity_log = ActivityLogModel(
            ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
            route = request.url,
            jti = "",
            username = data["username"],
            data = '{"username":"'+data["username"]+'","password":"'+data["password"]+'"}',
            remarks = "USER REGISTRATION ATTEMPT"
        )
        activity_log.save_to_db()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password'])
        )

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])

            whitelisted_token = WhitelistedTokenModel(jti = get_jti(access_token))
            whitelisted_token.add()

            whitelisted_token = WhitelistedTokenModel(jti = get_jti(refresh_token))
            whitelisted_token.add()

            activity_log = ActivityLogModel(
                ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                route = request.url,
                jti = get_jti(access_token),
                username = data["username"],
                data = '{"username":"'+data["username"]+'","password":"'+data["password"]+'"}',
                remarks = "CREATED NEW USER"
            )
            activity_log.save_to_db()

            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except Exception as e:
            return {'message': 'Error: ' + str(e)}, 500


class UserLogin(Resource):
    @ip_has_access
    def post(self):
        data = parser.parse_args()

        activity_log = ActivityLogModel(
            ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
            route = request.url,
            jti = "",
            username = data["username"],
            data = '{"username":"'+data["username"]+'","password":"'+data["password"]+'"}',
            remarks = "USER LOGIN ATTEMPT"
        )
        activity_log.save_to_db()

        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            #return {'message': 'User {} doesn\'t exist'.format(data['username'])}
            return {
                'message': 'Wrong credentials',
                'success': False
            }

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])

            raw_access_token = decode_token(access_token)
            raw_refresh_token = decode_token(refresh_token)

            at_exp = datetime.fromtimestamp(raw_access_token['exp']).strftime("%Y-%m-%d %H:%M:%S")
            rf_exp = datetime.fromtimestamp(raw_refresh_token['exp']).strftime("%Y-%m-%d %H:%M:%S")

            whitelisted_token = WhitelistedTokenModel(jti = get_jti(access_token), expiry_date=at_exp)
            whitelisted_token.add()

            whitelisted_token = WhitelistedTokenModel(jti = get_jti(refresh_token), expiry_date=rf_exp)
            whitelisted_token.add()

            activity_log = ActivityLogModel(
                ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                route = request.url,
                jti = get_jti(access_token),
                username = data["username"],
                data = '{"username":"'+data["username"]+'","password":"'+data["password"]+'"}',
                remarks = "USER LOGIN SUCCESS"
            )
            activity_log.save_to_db()

            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'success': True
            }
        else:
            return {
                'message': 'Wrong credentials',
                'success': False
            }


class UserLogoutAccess(Resource):
    @ip_has_access
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        identity = get_raw_jwt()['identity']
        try:
            activity_log = ActivityLogModel(
                ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                route = request.url,
                jti = jti,
                username = identity,
                data = "{"+"}",
                remarks = "USER LOGOUT ACCESS TOKEN"
            )
            activity_log.save_to_db()

            whitelisted_token = WhitelistedTokenModel.query.filter_by(jti=jti).first()

            if whitelisted_token:
                whitelisted_token.delete_in_db()

            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @ip_has_access
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        identity = get_raw_jwt()['identity']
        try:
            activity_log = ActivityLogModel(
                ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                route = request.url,
                jti = jti,
                username = identity,
                data = "{"+"}",
                remarks = "USER LOGOUT REFRESH TOKEN"
            )
            activity_log.save_to_db()

            whitelisted_token = WhitelistedTokenModel.query.filter_by(jti=jti).first()

            if whitelisted_token:
                whitelisted_token.delete_in_db()

            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @ip_has_access
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)

        whitelisted_token = WhitelistedTokenModel(jti = get_jti(access_token))
        whitelisted_token.add()

        activity_log = ActivityLogModel(
            ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
            route = request.url,
            jti = get_jti(access_token),
            username = current_user,
            data = "{"+"}",
            remarks = "REFRESHED ACCESS TOKEN"
        )
        activity_log.save_to_db()

        return {'access_token': access_token}


class AllUsers(Resource):
    @jwt_required
    def get(self):
        return UserModel.return_all()

    @jwt_required
    def delete(self):
        return {'message': 'Delete all users'}


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }
