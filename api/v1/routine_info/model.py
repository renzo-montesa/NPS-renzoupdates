from extensions import db
from flask_restful import marshal, fields as mfields


routine_info_fields = {
    'id': mfields.Integer,
    'routine_name': mfields.String,
    'routine_description': mfields.String,
    'routine_type_id': mfields.Integer,
    'routine_type_code': mfields.String,
    'routine_type_description': mfields.String
}


class RoutineInfoModel(db.Model):
    __tablename__ = 'routine_info'

    id = db.Column(db.Integer, primary_key = True)
    routine_name = db.Column(db.String(150))
    routine_description = db.Column(db.Text)
    routine_type_id = db.Column(db.Integer)
    routine_type_code = db.Column(db.String)
    routine_type_description = db.Column(db.String)

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
        return [marshal(r, routine_info_fields) for r in cls.query.all()]

    @classmethod
    def get_all_by_filter(cls, **kwargs):
        return [marshal(r, routine_info_fields) for r in cls.query.filter_by(**kwargs).all()]

    @classmethod
    def get_one_by_filter(cls, **kwargs):
        return marshal(cls.query.filter_by(**kwargs).first(), routine_info_fields)
