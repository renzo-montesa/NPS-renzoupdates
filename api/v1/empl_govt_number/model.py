from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


table_fields = {
    'id': mfields.Integer,
    'employee_id': mfields.Integer,
    'employee_number': mfields.String,
    'mandatory_code_id': mfields.Integer,
    'mandatory_code': mfields.String,
    'account_number': mfields.String,
    'is_exempt': mfields.Boolean,
    'basis': mfields.String
}


class EmplGovtNumberModel(db.Model):
    __tablename__ = 'empl_govt_number'

    id = db.Column(db.Integer, primary_key = True)
    employee_id = db.Column(db.Integer)
    employee_number = ""
    mandatory_code_id = db.Column(db.Integer)
    mandatory_code = ""
    account_number = db.Column(db.String)
    is_exempt = db.Column(db.Boolean)
    basis = db.Column(db.String)

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
    def get_by_filter(cls, client_db, **kwargs):
        client_session = get_client_session(client_db)
        return client_session.query(cls).filter_by(**kwargs).first(), client_session
