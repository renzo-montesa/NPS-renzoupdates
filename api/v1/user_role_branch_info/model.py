from extensions import db


class UserRoleBranchInfoModel(db.Model):
    __tablename__ = 'user_role_branch_info'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(100))
    role_id = db.Column(db.Integer)
    role_name = db.Column(db.String(50))
    branch_id = db.Column(db.Integer)
    branch_name = db.Column(db.String(254))

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
                'branch_name': x.branch_name
            }
        return {'branches': list(map(lambda x: to_json(x), UserRoleBranchInfoModel.query.all()))}

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
                'branch_name': x.branch_name
            }
        return {'branches': list(map(lambda x: to_json(x), UserRoleBranchInfoModel.query.filter_by(user_id = user_id).all()))}
    
    @classmethod
    def get_branches_by_user(cls, user_id):
        def to_json(x):
            return {
                'branch_id': x.branch_id,
                'branch_name': x.branch_name
            }
        return {'branches': list(map(lambda x: to_json(x), UserRoleBranchInfoModel.query.filter_by(user_id = user_id).all()))}

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
                'branch_name': x.branch_name
            }
        return {'branches': list(map(lambda x: to_json(x), RoleBranchInfoModel.query.filter_by(role_id = role_id).all()))}
    
    @classmethod
    def get_branches_by_role(cls, role_id):
        def to_json(x):
            return {
                'branch_id': x.branch_id,
                'branch_name': x.branch_name
            }
        return {'branches': list(map(lambda x: to_json(x), RoleBranchInfoModel.query.filter_by(role_id = role_id).all()))}
