from extensions import db
from flask_restful import marshal, fields as mfields


branch_fields = {
    'id': mfields.Integer,
    'client_id': mfields.Integer,
    'branch_code': mfields.String,
    'name': mfields.String,
    'address': mfields.String
}


class BranchModel(db.Model):
    __tablename__ = 'branch'

    id = db.Column(db.Integer, primary_key = True)
    client_id = db.Column(db.Integer)
    branch_code = db.Column(db.String)
    name = db.Column(db.String(254), nullable = False)
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
    def get_all_branches(cls):
        return [marshal(r, branch_fields) for r in cls.query.all()]

    @classmethod
    def get_all_by_filter(cls, **kwargs):
        return [marshal(r, branch_fields) for r in cls.query.filter_by(**kwargs).all()]

    @classmethod
    def get_all(cls):
        def to_json(x):
            return {
                'client_id': x.client_id,
                'name': x.name,
                'address': x.address
            }
        return {'branches': list(map(lambda x: to_json(x), BranchModel.query.all()))}
