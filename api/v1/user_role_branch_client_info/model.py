from extensions import db


class UserRoleBranchClientInfoModel(db.Model):
    __tablename__ = 'user_role_branch_client_info'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(100))
    role_id = db.Column(db.Integer)
    role_name = db.Column(db.String(50))
    branch_id = db.Column(db.Integer)
    branch_name = db.Column(db.String(254))
    client_id = db.Column(db.Integer)
    client_name = db.Column(db.String(254))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        def to_json(x):
            return {
                'id': x.id,
                'user_id': x.user_id,
                'username': x.username,
                'role_id': x.role_id,
                'role_name': x.role_name,
                'branch_id': x.branch_id,
                'branch_name': x.branch_name,
                'client_id': x.client_id,
                'client_name': x.client_name
            }
        return {'result': list(map(lambda x: to_json(x), UserRoleBranchClientInfoModel.query.all()))}

    @classmethod
    def get_by_user(cls, user_id):
        def to_json(x):
            return {
                'id': x.id,
                'user_id': x.user_id,
                'username': x.username,
                'role_id': x.role_id,
                'role_name': x.role_name,
                'branch_id': x.branch_id,
                'branch_name': x.branch_name,
                'client_id': x.client_id,
                'client_name': x.client_name
            }
        return {'result': list(map(lambda x: to_json(x), UserRoleBranchClientInfoModel.query.filter_by(user_id = user_id).all()))}
    
    @classmethod
    def get_by_role(cls, role_id):
        def to_json(x):
            return {
                'id': x.id,
                'user_id': x.user_id,
                'username': x.username,
                'role_id': x.role_id,
                'role_name': x.role_name,
                'branch_id': x.branch_id,
                'branch_name': x.branch_name,
                'client_id': x.client_id,
                'client_name': x.client_name
            }
        return {'result': list(map(lambda x: to_json(x), UserRoleBranchClientInfoModel.query.filter_by(role_id = role_id).all()))}
    
    @classmethod
    def get_clients_by_user(cls, user_id):
        def to_json(x):
            return {
                'client_id': x.client_id,
                'client_name': x.client_name
            }
        return {'result': list(map(lambda x: to_json(x), UserRoleBranchClientInfoModel.query.filter_by(user_id = user_id).group_by(UserRoleBranchClientInfoModel.client_id).all()))}
    
    @classmethod
    def get_clients_by_role(cls, role_id):
        def to_json(x):
            return {
                'client_id': x.client_id,
                'client_name': x.client_name
            }
        return {'result': list(map(lambda x: to_json(x), UserRoleBranchClientInfoModel.query.filter_by(role_id = role_id).group_by(UserRoleBranchClientInfoModel.client_id).all()))}
