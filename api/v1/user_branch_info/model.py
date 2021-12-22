from extensions import db


class UserBranchInfoModel(db.Model):
    __tablename__ = 'user_branch_info'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(100))
    branch_id = db.Column(db.Integer)
    branch_name = db.Column(db.String(254))
    client_id = db.Column(db.Integer)
    address = db.Column(db.String(254))

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
                'branch_id': x.branch_id,
                'branch_name': x.branch_name,
                'client_id': x.client_id,
                'address': x.address
            }
        return {'result': list(map(lambda x: to_json(x), cls.query.all()))}

    @classmethod
    def get_by_user(cls, user_id):
        def to_json(x):
            return {
                'id': x.id,
                'user_id': x.user_id,
                'username': x.username,
                'branch_id': x.branch_id,
                'branch_name': x.branch_name,
                'client_id': x.client_id,
                'address': x.address
            }
        return {'result': list(map(lambda x: to_json(x), cls.query.filter_by(user_id = user_id).all()))}
    
    @classmethod
    def get_branches_by_user(cls, user_id):
        def to_json(x):
            return {
                'id': x.branch_id,
                'name': x.branch_name,
                'client_id': x.client_id,
                'address': x.address
            }
        return {'result': list(map(lambda x: to_json(x), cls.query.filter_by(user_id = user_id).all()))}
    
    @classmethod
    def get_branches_by_username(cls, username):
        def to_json(x):
            return {
                'id': x.branch_id,
                'name': x.branch_name,
                'client_id': x.client_id,
                'address': x.address
            }
        return {'result': list(map(lambda x: to_json(x), cls.query.filter_by(username = username).group_by(cls.branch_id).all()))}
    
    @classmethod
    def get_branches_by_username_and_client(cls, username, client_id):
        def to_json(x):
            return {
                'id': x.branch_id,
                'name': x.branch_name,
                'client_id': x.client_id,
                'address': x.address
            }
        return {'result': list(map(lambda x: to_json(x), cls.query.filter_by(username = username, client_id = client_id).group_by(cls.branch_id).all()))}
    
    @classmethod
    def has_user_branch_access(cls, username, branch_id):
        branch = cls.query.filter_by(username = username, branch_id = branch_id).all()

        return branch
