from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


loan_info_fields = {
    'id': mfields.Integer,
    'employee_id': mfields.Integer,
    'schedule_id': mfields.Integer,
    'schedule_code': mfields.String,
    'loan_code_id': mfields.Integer,
    'pay_element_id': mfields.Integer,
    'pay_element_code': mfields.String,
    'pay_element_description': mfields.String,
    'loan_type_id': mfields.Integer,
    'loan_type_code': mfields.String,
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


class LoanInfoModel(db.Model):
    __tablename__ = 'loan_info'

    id = db.Column(db.Integer, primary_key = True)
    employee_id = db.Column(db.Integer)
    schedule_id = db.Column(db.Integer)
    schedule_code = db.Column(db.String)
    loan_code_id = db.Column(db.Integer)
    pay_element_id = db.Column(db.Integer)
    pay_element_code = db.Column(db.String)
    pay_element_description = db.Column(db.String)
    loan_type_id = db.Column(db.Integer)
    loan_type_code = db.Column(db.String)
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
    def get_active_loans(cls, client_db):
        client_session = get_client_session(client_db)
        records = client_session.query(cls).filter(cls.is_suspended==False, cls.is_stopped==False, cls.outstanding_balance!=0.00).all()
        client_session.close()
        return [marshal(r, loan_info_fields) for r in records]
