from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


table_fields = {
    'id': mfields.Integer,
    'report_id': mfields.Integer,
    'tablename': mfields.String,
    'key': mfields.String,
    'field': mfields.String,
    'description': mfields.String,
    'field_order': mfields.String
}


class ReportFieldModel(db.Model):
    __tablename__ = 'report_field'

    id = db.Column(db.Integer, primary_key = True)
    report_id = db.Column(db.Integer)
    tablename = db.Column(db.String)
    key = db.Column(db.String)
    field = db.Column(db.String)
    description = db.Column(db.String)
    field_order = db.Column(db.Integer)

    def save_to_db(self, client_db):
        client_session = get_client_session(client_db)
        client_session.add(self)
        client_session.commit()

    def commit_to_db(self, client_session):
        client_session.commit()

    def delete_in_db(self, client_db):
        client_session = get_client_session(client_db)
        client_session.delete(self)
        client_session.commit()

    @classmethod
    def get_all(cls, client_db):
        client_session = get_client_session(client_db)
        return [marshal(r, table_fields) for r in client_session.query(cls).all()]

    @classmethod
    def get_all_by_filter(cls, client_db, **kwargs):
        client_session = get_client_session(client_db)
        return [marshal(r, table_fields) for r in client_session.query(cls).filter_by(**kwargs).order_by(cls.field_order.asc()).all()]
