from extensions import db
from sqlalchemy import or_
from flask_restful import marshal, fields as mfields
from system_core.helper.array_to_dict import (array_to_dict_by_key)
from api.v1.helper.multi_db_management import get_client_session


employee_fields = {
    'id': mfields.Integer,
    'branch_id': mfields.Integer,
    'employee_number': mfields.String,
    'firstname': mfields.String,
    'middlename': mfields.String,
    'lastname': mfields.String,
    'suffix': mfields.String,
    'telephone': mfields.String,
    'sex': mfields.String,
    'birthday': mfields.String,
    'civil_status_id': mfields.Integer,
    'civil_status_code': mfields.String,
    'civil_status_description': mfields.String,
    'nationality_id': mfields.Integer,
    'nationality_code': mfields.String,
    'nationality_description': mfields.String,
    'hired_date': mfields.String,
    'regularization_date': mfields.String,
    'pagibig_additional': mfields.Float,
    'is_pagibig_max': mfields.Boolean,
    'rate_hour': mfields.Float,
    'rate_day': mfields.Float,
    'rate_month': mfields.Float,
    'timesheet_exempt': mfields.Boolean,
    'rank_id': mfields.Integer,
    'rank_code': mfields.String,
    'rank_description': mfields.String,
    'section_id': mfields.Integer,
    'section_code': mfields.String,
    'section_description': mfields.String,
    'department_id': mfields.Integer,
    'department_code': mfields.String,
    'department_description': mfields.String,
    'employment_status_id': mfields.Integer,
    'employment_status_code': mfields.String,
    'employment_status_description': mfields.String,
    'job_type_id': mfields.Integer,
    'job_type_code': mfields.String,
    'job_type_description': mfields.String,
    'level_id': mfields.Integer,
    'level_code': mfields.String,
    'level_description': mfields.String,
    'pay_type': mfields.String,
    'pay_code': mfields.String,
    'prev_company_name': mfields.String,
    'prev_address': mfields.String,
    'prev_telephone': mfields.String,
    'prev_tin': mfields.String,
    'prev_rate': mfields.Float,
    'pytd_taxable_earning': mfields.Float,
    'pytd_nontax_earning': mfields.Float,
    'pytd_nontax_bonus': mfields.Float,
    'pytd_taxable_bonus': mfields.Float,
    'pytd_wtax': mfields.Float,
    'pytd_union': mfields.Float,
    'pytd_sss': mfields.Float,
    'pytd_med': mfields.Float,
    'pytd_pagib': mfields.Float
}


employee_basic_fields = {
    'id': mfields.Integer,
    'employee_number': mfields.String,
    'firstname': mfields.String,
    'middlename': mfields.String,
    'lastname': mfields.String,
    'section_code': mfields.String,
    'department_code': mfields.String,
}


class EmployeeInfoModel(db.Model):
    __bind_key__ = 'client_db'
    __tablename__ = 'employee_info'

    id = db.Column(db.Integer, primary_key = True)
    branch_id = db.Column(db.Integer)
    employee_number = db.Column(db.String(20))
    firstname = db.Column(db.String(50))
    middlename = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    suffix = db.Column(db.String)
    telephone = db.Column(db.String(20))
    sex = db.Column(db.String(1))
    birthday = db.Column(db.String)
    civil_status_id = db.Column(db.Integer)
    civil_status_code = db.Column(db.String(10))
    civil_status_description = db.Column(db.String(100))
    nationality_id = db.Column(db.Integer)
    nationality_code = db.Column(db.String(10))
    nationality_description = db.Column(db.String(100))
    hired_date = db.Column(db.String)
    regularization_date = db.Column(db.String)
    pagibig_additional = db.Column(db.Numeric(14,2))
    is_pagibig_max = db.Column(db.Boolean)
    rate_hour = db.Column(db.Numeric(14,4))
    rate_day = db.Column(db.Numeric(14,2))
    rate_month = db.Column(db.Numeric(14,2))
    timesheet_exempt = db.Column(db.Boolean)
    rank_id = db.Column(db.Integer)
    rank_code = db.Column(db.String(10))
    rank_description = db.Column(db.String(100))
    section_id = db.Column(db.Integer)
    section_code = db.Column(db.String(10))
    section_description = db.Column(db.String(100))
    department_id = db.Column(db.Integer)
    department_code = db.Column(db.String(10))
    department_description = db.Column(db.String(100))
    employment_status_id = db.Column(db.Integer)
    employment_status_code = db.Column(db.String(10))
    employment_status_description = db.Column(db.String(100))
    job_type_id = db.Column(db.Integer)
    job_type_code = db.Column(db.String(10))
    job_type_description = db.Column(db.String(100))
    level_id = db.Column(db.Integer)
    level_code = db.Column(db.String(10))
    level_description = db.Column(db.String(100))
    pay_type = db.Column(db.String)
    pay_code = db.Column(db.String)
    prev_company_name = db.Column(db.String)
    prev_address = db.Column(db.String)
    prev_telephone = db.Column(db.String)
    prev_tin = db.Column(db.String)
    prev_rate = db.Column(db.Numeric(14,2))
    pytd_taxable_earning = db.Column(db.Numeric(14,2))
    pytd_nontax_earning = db.Column(db.Numeric(14,2))
    pytd_nontax_bonus = db.Column(db.Numeric(14,2))
    pytd_taxable_bonus = db.Column(db.Numeric(14,2))
    pytd_wtax = db.Column(db.Numeric(14,2))
    pytd_union = db.Column(db.Numeric(14,2))
    pytd_sss = db.Column(db.Numeric(14,2))
    pytd_med = db.Column(db.Numeric(14,2))
    pytd_pagib = db.Column(db.Numeric(14,2))

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
    def get_all_employees(cls, client_db):
        client_session = get_client_session(client_db)
        records = client_session.query(cls).all()
        client_session.close()
        return [marshal(r, employee_fields) for r in records]
    
    @classmethod
    def get_active_employees(cls, client_db):
        client_session = get_client_session(client_db)
        records = client_session.query(cls).filter(cls.employment_status_code.in_(('1','2','3','4','5'))).all()
        client_session.close()
        return [marshal(r, employee_fields) for r in records]
    
    @classmethod
    def get_no_prev_employer_data(cls, client_db):
        client_session = get_client_session(client_db)
        records = client_session.query(cls).filter(or_(cls.pytd_taxable_earning == 0.00, cls.pytd_taxable_earning == None)).order_by(cls.employee_number).all()
        client_session.close()
        return [marshal(r, employee_fields) for r in records]


    @classmethod
    def get_employees_basic_info(cls, client_db):
        client_session = get_client_session(client_db)
        records = client_session.query(cls).all()
        client_session.close()
        return [marshal(r, employee_basic_fields) for r in records]
