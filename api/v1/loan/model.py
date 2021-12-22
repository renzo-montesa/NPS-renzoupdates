from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


recurring_element_fields = {
    'id': mfields.Integer,
    'employee_id': mfields.Integer,
    'employee_number': mfields.String,
    'schedule_id': mfields.Integer,
    'schedule_code': mfields.String,
    'loan_code_id': mfields.Integer,
    'loan_code': mfields.String,
    'loan_date': mfields.String,
    'first_deduction': mfields.String,
    'loan_amount': mfields.Float,
    'principal_amount': mfields.Float,
    'outstanding_balance': mfields.Float,
    'installment_amount': mfields.Float,
    'is_suspended': mfields.Boolean,
    'is_stopped': mfields.Boolean,
    'no_of_installment': mfields.Integer,
    'remarks': mfields.String,
    'last_installment_no': mfields.Integer
}


class LoanModel(db.Model):
    __tablename__ = 'loan'

    id = db.Column(db.Integer, primary_key = True)
    employee_id = db.Column(db.Integer)
    employee_number = ""
    schedule_id = db.Column(db.Integer)
    schedule_code = ""
    loan_code_id = db.Column(db.Integer)
    loan_code = ""
    loan_date = db.Column(db.String)
    first_deduction = db.Column(db.String)
    loan_amount = db.Column(db.Numeric(14,2))
    principal_amount = db.Column(db.Numeric(14,2))
    outstanding_balance = db.Column(db.Numeric(14,2))
    installment_amount = db.Column(db.Numeric(14,2))
    is_suspended = db.Column(db.Boolean)
    is_stopped = db.Column(db.Boolean)
    no_of_installment = db.Column(db.Integer)
    remarks = db.Column(db.String)
    last_installment_no = db.Column(db.Integer)

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
