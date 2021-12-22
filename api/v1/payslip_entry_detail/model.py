from extensions import db
from sqlalchemy import text
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


payslip_entry_detail_fields = {
    'id': mfields.Integer,
    'payslip_id': mfields.Integer,
    'employee_id': mfields.Integer,
    'employee_number': mfields.String,
    'payroll_period_id': mfields.Integer,
    'period_start': mfields.String,
    'period_end': mfields.String,
    'transaction_start': mfields.String,
    'transaction_end': mfields.String,
    'pay_element_id': mfields.Integer,
    'pay_element_code': mfields.String,
    'amount': mfields.Float,
    'is_finalized': mfields.Boolean
}


payslip_entry_info_fields = {
    'id': mfields.Integer,
    'payslip_id': mfields.Integer,
    'pay_element_id': mfields.Integer,
    'pay_element_code': mfields.String,
    'amount': mfields.Float
}


payslip_entry_employees_fields = {
    'employee_id': mfields.Integer,
    'employee_number': mfields.String
}


monthly_earning_fields = {
    'employee_id': mfields.Integer,
    'employee_number': mfields.String,
    'pay_element_id': mfields.Integer,
    'pay_element_code': mfields.String,
    'amount': mfields.Float
}


fbt_employee_earning_fields = {
    'employee_id': mfields.Integer,
    'employee_number': mfields.String,
    'pay_element_id': mfields.Integer,
    'pay_element_code': mfields.String,
}


pay_elements_fields = {
    'pay_element_id': mfields.Integer,
    'pay_element_code': mfields.String
}


class PayslipEntryDetailModel(db.Model):
    __tablename__ = 'payslip_entry_detail'

    id = db.Column(db.Integer, primary_key = True)
    payslip_id = db.Column(db.Integer)
    employee_id = db.Column(db.Integer)
    employee_number = db.Column(db.String)
    payroll_period_id = db.Column(db.Integer)
    period_start = db.Column(db.String)
    period_end = db.Column(db.String)
    transaction_start = db.Column(db.String)
    transaction_end = db.Column(db.String)
    pay_element_id = db.Column(db.Integer)
    pay_element_code = db.Column(db.String(50))
    amount = db.Column(db.Numeric(14,2))
    is_finalized = db.Column(db.Boolean)

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
        return [marshal(r, payslip_entry_detail_fields) for r in client_session.query(cls).filter_by(payroll_period_id=payroll_period_id).all()]

    @classmethod
    def get_all_by_filter(cls, client_db, **kwargs):
        client_session = get_client_session(client_db)
        return [marshal(r, payslip_entry_detail_fields) for r in client_session.query(cls).filter_by(**kwargs).all()]

    
    @classmethod
    def get_historical_payslip_entries_by_employee_id(cls, client_db, employee_id):
        client_session = get_client_session(client_db)
        return [marshal(r, payslip_entry_detail_fields) for r in client_session.query(cls).filter(cls.is_finalized==True, cls.employee_id==employee_id).all()]

    
    @classmethod
    def get_earnings_by_month(cls, month, year):
        start_date = str(year) + "-" + str(month) + "-01"
        end_date = str(year) + "-" + str(month) + "-31"
        stmt = "SELECT id, payslip_id, employee_id, employee_number, payroll_period_id, "
        stmt += "period_start, period_end, transaction_start, transaction_end, "
        stmt += "pay_element_id, pay_element_code, SUM(amount) AS AMOUNT "
        stmt += "FROM payslip_entry_detail "
        stmt += "WHERE period_start >= :start_date AND period_start <= :end_date "
        stmt += "GROUP BY employee_id ORDER BY employee_number"
        payslip_entries = cls.query.from_statement(text(stmt)).params(start_date=start_date, end_date=end_date).all()
        return [marshal(r, payslip_entry_detail_fields) for r in payslip_entries]

    
    @classmethod
    def get_employees_with_earnings_by_quarter(cls, month, year):
        start_date = str(year) + "-" + str(month) + "-01"
        end_date = str(year) + "-" + str(month+2) + "-31"
        stmt = "SELECT id, payslip_id, employee_id, employee_number, payroll_period_id, "
        stmt += "period_start, period_end, transaction_start, transaction_end, "
        stmt += "pay_element_id, pay_element_code, SUM(amount) AS AMOUNT "
        stmt += "FROM payslip_entry_detail "
        stmt += "WHERE period_start >= :start_date AND period_start <= :end_date "
        stmt += "GROUP BY employee_id ORDER BY employee_number"
        payslip_entries = cls.query.from_statement(text(stmt)).params(start_date=start_date, end_date=end_date).all()
        return [marshal(r, payslip_entry_employees_fields) for r in payslip_entries]


    @classmethod
    def get_fbt_earnings_by_month(cls, month, year):
        start_date = str(year) + "-" + str(month) + "-01"
        end_date = str(year) + "-" + str(month) + "-31"
        stmt = "SELECT id, payslip_id, employee_id, employee_number, payroll_period_id, "
        stmt += "period_start, period_end, transaction_start, transaction_end, "
        stmt += "pay_element_id, pay_element_code, SUM(amount) AS AMOUNT "
        stmt += "FROM payslip_entry_detail "
        stmt += "WHERE period_start >= :start_date AND period_start <= :end_date "
        stmt += "AND pay_element_id IN "
        stmt += "(SELECT DISTINCT id FROM pay_element_property_info "
        stmt += "WHERE pay_element_property='is_fbt' AND pay_element_value='TRUE') "
        stmt += "GROUP BY employee_id, pay_element_id ORDER BY employee_number, pay_element_code"
        payslip_entries = cls.query.from_statement(text(stmt)).params(start_date=start_date, end_date=end_date).all()
        return [marshal(r, payslip_entry_detail_fields) for r in payslip_entries]


    @classmethod
    def get_fbt_employees_by_quarter(cls, month, year):
        start_date = str(year) + "-" + str(month) + "-01"
        end_date = str(year) + "-" + str(month+2) + "-31"
        stmt = "SELECT id, payslip_id, employee_id, employee_number, payroll_period_id, "
        stmt += "period_start, period_end, transaction_start, transaction_end, "
        stmt += "pay_element_id, pay_element_code, SUM(amount) AS AMOUNT "
        stmt += "FROM payslip_entry_detail "
        stmt += "WHERE period_start >= :start_date AND period_start <= :end_date "
        stmt += "AND pay_element_id IN "
        stmt += "(SELECT DISTINCT id FROM pay_element_property_info "
        stmt += "WHERE pay_element_property='is_fbt' AND pay_element_value='TRUE') "
        stmt += "GROUP BY employee_id, pay_element_id ORDER BY employee_number, pay_element_code"
        payslip_entries = cls.query.from_statement(text(stmt)).params(start_date=start_date, end_date=end_date).all()
        return [marshal(r, fbt_employee_earning_fields) for r in payslip_entries]
    

    @classmethod
    def get_pay_elements_by_payroll_period_id(cls, payroll_period_id):
        stmt = "SELECT id, payslip_id, employee_id, employee_number, payroll_period_id, "
        stmt += "period_start, period_end, transaction_start, transaction_end, "
        stmt += "pay_element_id, pay_element_code, SUM(amount) AS AMOUNT "
        stmt += "FROM payslip_entry_detail "
        stmt += "WHERE payroll_period_id >= :payroll_period_id "
        stmt += "GROUP BY pay_element_id ORDER BY employee_number, pay_element_code"
        payslip_entries = cls.query.from_statement(text(stmt)).params(payroll_period_id=payroll_period_id).all()
        return [marshal(r, fbt_employee_earning_fields) for r in payslip_entries]

    @classmethod
    def get_distinct_pec_by_ppid(cls, client_db, payroll_period_id):
        client_session = get_client_session(client_db)
        stmt = "SELECT id, pay_element_code "
        stmt += "FROM payslip_entry_detail "
        stmt += "WHERE payroll_period_id=:payroll_period_id "
        stmt += "GROUP BY pay_element_code ORDER BY pay_element_code"
        return [r.pay_element_code for r in client_session.query(cls).from_statement(text(stmt)).params(payroll_period_id=payroll_period_id).all()]