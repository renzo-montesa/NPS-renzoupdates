from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


recurring_element_fields = {
    'id': mfields.Integer,
    'pay_element_id': mfields.Integer,
    'pay_element_code': mfields.String,
    'pay_element_description': mfields.String,
    'loan_type_id': mfields.Integer,
    'loan_type_code': mfields.String,
    'loan_type_description': mfields.String,
    'is_zero_out': mfields.Boolean
}


class LoanCodeInfoModel(db.Model):
    __bind_key__ = 'client_db'
    __tablename__ = 'loan_code_info'

    id = db.Column(db.Integer, primary_key = True)
    pay_element_id = db.Column(db.Integer)
    pay_element_code = db.Column(db.String)
    pay_element_description = db.Column(db.String)
    loan_type_id = db.Column(db.Integer)
    loan_type_code = db.Column(db.String)
    loan_type_description = db.Column(db.String)
    is_zero_out = db.Column(db.Boolean)

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
        return [marshal(r, recurring_element_fields) for r in client_session.query(cls).all()]

    @classmethod
    def get_by_filter(cls, client_db, **kwargs):
        client_session = get_client_session(client_db)
        return client_session.query(cls).filter_by(**kwargs).first(), client_session
