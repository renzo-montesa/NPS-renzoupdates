from extensions import db


class RoleBranchClientInfoModel(db.Model):
    __tablename__ = 'role_branch_client_info'

    id = db.Column(db.Integer, primary_key = True)
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
                'role_id': x.role_id,
                'role_name': x.role_name,
                'branch_id': x.branch_id,
                'branch_name': x.branch_name,
                'client_id': x.client_id,
                'client_name': x.client_name
            }
        return {'result': list(map(lambda x: to_json(x), RoleBranchClientInfoModel.query.all()))}

    @classmethod
    def get_by_role(cls, role_id):
        def to_json(x):
            return {
                'id': x.id,
                'role_id': x.role_id,
                'role_name': x.role_name,
                'branch_id': x.branch_id,
                'branch_name': x.branch_name,
                'client_id': x.client_id,
                'client_name': x.client_name
            }
        return {'result': list(map(lambda x: to_json(x), RoleBranchClientInfoModel.query.filter_by(role_id = role_id).all()))}
    
    @classmethod
    def get_clients_by_role(cls, role_id):
        def to_json(x):
            return {
                'client_id': x.client_id,
                'client_name': x.client_name
            }
        return {'result': list(map(lambda x: to_json(x), RoleBranchClientInfoModel.query.filter_by(role_id = role_id).group_by(RoleBranchClientInfoModel.client_id).all()))}
