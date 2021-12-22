from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


table_fields = {
    'id': mfields.Integer,
    'branch_id': mfields.Integer,
    'bank_code': mfields.String,
    'bank_name': mfields.String,
    'account_number': mfields.String
}


class BankModel(db.Model):
    __tablename__ = 'bank'

    id = db.Column(db.Integer, primary_key = True)
    branch_id = db.Column(db.Integer)
    bank_code = db.Column(db.String)
    bank_name = db.Column(db.String)
    account_number = db.Column(db.String)

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
