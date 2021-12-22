from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


table_fields = {
    'id': mfields.Integer,
    'loan_id': mfields.Integer,
    'deduction_date': mfields.String,
    'amount': mfields.Float,
    'installment_no': mfields.Integer,
    'outstanding_balance': mfields.Float,
    'is_posted': mfields.Boolean,
    'is_hidden': mfields.Boolean
}


class LoanPaymentModel(db.Model):
    __tablename__ = 'loan_payment'

    id = db.Column(db.Integer, primary_key = True)
    loan_id = db.Column(db.Integer)
    deduction_date = db.Column(db.String)
    amount = db.Column(db.Numeric(14,2))
    installment_no = db.Column(db.Integer)
    outstanding_balance = db.Column(db.Numeric(14,2))
    is_posted = db.Column(db.Boolean)
    is_hidden = db.Column(db.Boolean)

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
