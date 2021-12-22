from extensions import db
from flask_jwt_extended import (get_jwt_identity)


class UserRolePermissionInfoModel(db.Model):
    __tablename__ = 'user_role_permission_info'

    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    role_id = db.Column(db.Integer, primary_key = True)
    role_name = db.Column(db.String(255))
    permission_id = db.Column(db.Integer, primary_key = True)
    permission_name = db.Column(db.String(255))

    @classmethod
    def has_user_permission(cls, username, permission_name):
        user_permission = cls.query.filter_by(username = username, permission_name = permission_name).all()

        return user_permission


def permission_required(permission_name):
    def wrap(func):
        def wrapper(*args, **kwargs):
            username = get_jwt_identity()
            if UserRolePermissionInfoModel.has_user_permission(username, permission_name):
                return func(*args, **kwargs)
            else:
                return {'message': 'Unauthorized access'}, 403
        return wrapper
    return wrap
