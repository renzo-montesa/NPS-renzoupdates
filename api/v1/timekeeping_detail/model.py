from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


timekeeping_detail_fields = {
    'id': mfields.Integer,
    'payslip_id': mfields.Integer,
    'employee_id': mfields.Integer,
    'employee_number': mfields.String,
    'payroll_period_id': mfields.Integer,
    'tk_element_id': mfields.Integer,
    'tk_element_code': mfields.String,
    'hours': mfields.Float
}


class TimekeepingDetailModel(db.Model):
    __tablename__ = 'timekeeping_detail'

    id = db.Column(db.Integer, primary_key = True)
    payslip_id = db.Column(db.Integer)
    employee_id = db.Column(db.Integer)
    employee_number = db.Column(db.String)
    payroll_period_id = db.Column(db.Integer)
    tk_element_id = db.Column(db.Integer)
    tk_element_code = db.Column(db.String(50))
    hours = db.Column(db.Numeric(14,4))

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
    def get_all_by_payroll_period_id(cls, client_db, payroll_period_id):
        client_session = get_client_session(client_db)
        return [marshal(r, timekeeping_detail_fields) for r in client_session.query(cls).filter_by(payroll_period_id=payroll_period_id).all()]
    
    @classmethod
    def get_all_by_filter(cls, client_db, **kwargs):
        client_session = get_client_session(client_db)
        return [marshal(r, timekeeping_detail_fields) for r in client_session.query(cls).filter_by(**kwargs).all()]
