from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


payslip_info_fields = {
    'id': mfields.Integer,
    'employee_id': mfields.Integer,
    'employee_number': mfields.String,
    'firstname': mfields.String,
    'middlename': mfields.String,
    'lastname': mfields.String,
    'payroll_period_id': mfields.Integer,
    'period_start': mfields.String,
    'period_end': mfields.String,
    'transaction_start': mfields.String,
    'transaction_end': mfields.String,
    'net_pay': mfields.Float,
    'take_home': mfields.Float
}


class PayslipInfoModel(db.Model):
    __bind_key__ = 'client_db'
    __tablename__ = 'payslip_info'

    id = db.Column(db.Integer, primary_key = True)
    employee_id = db.Column(db.Integer)
    employee_number = db.Column(db.String)
    firstname = db.Column(db.String)
    middlename = db.Column(db.String)
    lastname = db.Column(db.String)
    payroll_period_id = db.Column(db.Integer)
    period_start = db.Column(db.String)
    period_end = db.Column(db.String)
    transaction_start = db.Column(db.String)
    transaction_end = db.Column(db.String)
    net_pay = db.Column(db.Numeric(14,2))
    take_home = db.Column(db.Numeric(14,2))

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
    def get_payslips_by_payroll_period_id(cls, client_db, payroll_period_id):
        client_session = get_client_session(client_db)
        return [marshal(r, payslip_info_fields) for r in client_session.query(cls).filter_by(payroll_period_id=payroll_period_id).all()]
    
    @classmethod
    def get_by_filter(cls, client_db, **kwargs):
        client_session = get_client_session(client_db)
        return client_session.query(cls).filter_by(**kwargs).first(), client_session

    @classmethod
    def get_all_by_filter(cls, client_db, **kwargs):
        client_session = get_client_session(client_db)
        records = client_session.query(cls).filter_by(**kwargs).all()
        client_session.close()
        return [marshal(r, payslip_info_fields) for r in records]
