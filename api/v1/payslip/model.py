from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


payslip_fields = {
    'id': mfields.Integer,
    'employee_id': mfields.Integer,
    'payroll_period_id': mfields.Integer,
    'net_pay': mfields.Float,
    'take_home': mfields.Float,
    'is_finalized': mfields.Boolean
}


class PayslipModel(db.Model):
    __bind_key__ = 'client_db'
    __tablename__ = 'payslip'

    id = db.Column(db.Integer, primary_key = True)
    employee_id = db.Column(db.Integer)
    payroll_period_id = db.Column(db.Integer)
    net_pay = db.Column(db.Numeric(14,2))
    take_home = db.Column(db.Numeric(14,2))
    is_finalized = db.Column(db.Boolean)
    """employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    employee = db.relationship('EmployeeModel', backref='employee')"""

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

    def close(self, client_db):
        client_session = get_client_session(client_db)
        client_session.close()

    @classmethod
    def getById(cls, client_db, id):
        client_session = get_client_session(client_db)
        return client_session.query(cls).filter_by(id=id).first(), client_session

    @classmethod
    def deleteByPayrollPeriod(cls, client_db, payroll_period_id):
        client_session = get_client_session(client_db)
        payslips = client_session.query(cls).filter_by(payroll_period_id=payroll_period_id).all()
        for payslip in payslips:
            payslip.net_pay = 0.00
            payslip.take_home = 0.00
            payslip.commit_to_db(client_session)
        client_session.close()

    @classmethod
    def getPayslipsByPayrollPeriodId(cls, client_db, payroll_period_id):
        client_session = get_client_session(client_db)
        records = client_session.query(cls).filter_by(payroll_period_id=payroll_period_id).all()
        client_session.close()
        return [marshal(r, payslip_fields) for r in records]

    @classmethod
    def finalizeByFilter(cls, client_db, **kwargs):
        client_session = get_client_session(client_db)
        client_session.query(cls).filter_by(**kwargs).update({cls.is_finalized: 1})
        client_session.commit()
        client_session.close()

    """@classmethod
    def getPayslips(cls):
        def to_json(x):
            return {
                'id': x.id,
                'employee': {
                    'employee_id': x.employee_id,
                    'employee_number': x.employee.employee_number,
                    'firstname': x.employee.firstname,
                    'middlename': x.employee.middlename,
                    'lastname': x.employee.lastname
                }
            }
        return {'payslips': list(map(lambda x: to_json(x), PayslipModel.query.all()))}"""
