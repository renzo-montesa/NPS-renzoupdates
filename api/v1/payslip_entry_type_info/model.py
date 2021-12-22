from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


payslip_entry_type_info_fields = {
    'id': mfields.Integer,
    'payslip_id': mfields.Integer,
    'pay_element_id': mfields.Integer,
    'pay_element_code': mfields.String,
    'multiplier': mfields.Float,
    'pay_element_type_id': mfields.Integer,
    'pay_element_type_code': mfields.String,
    'amount': mfields.Float
}


class PayslipEntryTypeInfoModel(db.Model):
    __bind_key__ = 'client_db'
    __tablename__ = 'payslip_entry_type_info'

    id = db.Column(db.Integer, primary_key = True)
    payslip_id = db.Column(db.Integer)
    pay_element_id = db.Column(db.Integer)
    pay_element_code = db.Column(db.String(50))
    multiplier = db.Column(db.Numeric(10,2))
    pay_element_type_id = db.Column(db.Integer)
    pay_element_type_code = db.Column(db.String(50))
    amount = db.Column(db.Numeric(14,2))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_total_earnings_by_payslip_id(cls, client_db, payslip_id):
        client_session = get_client_session(client_db)
        result = client_session.query(db.func.sum(cls.amount * cls.multiplier).label('amount')).filter_by(payslip_id=payslip_id, pay_element_type_code="earning").first()[0]
        client_session.close()
        return result
    
    @classmethod
    def get_total_deductions_by_payslip_id(cls, client_db, payslip_id):
        client_session = get_client_session(client_db)
        result = client_session.query(db.func.sum(cls.amount * cls.multiplier).label('amount')).filter_by(payslip_id=payslip_id, pay_element_type_code="deduction").first()[0]
        client_session.close()
        return result

    @classmethod
    def get_sum_by_filter(cls, client_db, **kwargs):
        client_session = get_client_session(client_db)
        result = client_session.query(db.func.sum(cls.amount * cls.multiplier).label('amount')).filter_by(**kwargs).first()[0]
        client_session.close()
        return result