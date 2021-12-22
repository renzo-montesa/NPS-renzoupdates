from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


employee_fields = {
    'id': mfields.Integer,
    'branch_id': mfields.Integer,
    'employee_number': mfields.String,
    'swipeno': mfields.String,
    'firstname': mfields.String,
    'middlename': mfields.String,
    'lastname': mfields.String,
    'suffix': mfields.String,
    'address': mfields.String,
    'telephone': mfields.String,
    'sex': mfields.String,
    'birthday': mfields.String,
    'civil_status_id': mfields.Integer,
    'nationality_id': mfields.Integer,
    'hired_date': mfields.String,
    'regularization_date': mfields.String,
    'is_union_member': mfields.Boolean,
    'resign_date': mfields.String,
    'pagibig_additional': mfields.Float,
    'is_pagibig_max': mfields.Boolean,
    'rate_min': mfields.Float,
    'rate_hour': mfields.Float,
    'rate_day': mfields.Float,
    'rate_month': mfields.Float,
    'timesheet_exempt': mfields.Boolean,
    'rank_id': mfields.Integer,
    'section_id': mfields.Integer,
    'employment_status_id': mfields.Integer,
    'job_type_id': mfields.Integer,
    'level_id': mfields.Integer,
    'position': mfields.String,
    'pay_type': mfields.String,
    'pay_code': mfields.String,
    'gl_account': mfields.String,
    'supervisor': mfields.String,
    'ndiff1_rate': mfields.Float,
    'ndiff2_rate': mfields.Float,
    'ot_rate': mfields.Float,
    'tardy_rate': mfields.Float,
    'ut_rate': mfields.Float,
    'absent_rate': mfields.Float,
    'income_out': mfields.Float,
    'cola_rate': mfields.Float,
    'tax_table': mfields.String,
    'tax_unit': mfields.String,
    'tax_method': mfields.String,
    'filed_date': mfields.String,
    'approved_by': mfields.String,
    'is_suspended': mfields.Boolean,
    'suspend_date': mfields.String,
    'percentage': mfields.Float,
    'evaluator': mfields.String,
    'evaluation_date': mfields.String,
    'old_rate': mfields.Float,
    'old_position': mfields.String,
    'old_civil_status': mfields.String,
    'email': mfields.String,
    'is_inc_alpha': mfields.Boolean,
    'is_mwe': mfields.Boolean,
    'no_period': mfields.Integer,
    'dratemonth': mfields.Float
}

employee_id_fields = {
    'id': mfields.Integer,
    'employee_number': mfields.String
}

basic_info_fields = {
    'id': mfields.Integer,
    'branch_id': mfields.Integer,
    'employee_number': mfields.String,
    'firstname': mfields.String,
    'middlename': mfields.String,
    'lastname': mfields.String,
    'suffix': mfields.String,
}


class EmployeeModel(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key = True)
    branch_id = db.Column(db.Integer)
    swipeno = db.Column(db.String)
    employee_number = db.Column(db.String(20))
    firstname = db.Column(db.String(100))
    middlename = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    suffix = db.Column(db.String)
    address = db.Column(db.String)
    telephone = db.Column(db.String)
    sex = db.Column(db.String)
    birthday = db.Column(db.String)
    civil_status_id = db.Column(db.Integer)
    nationality_id = db.Column(db.Integer)
    hired_date = db.Column(db.String)
    regularization_date = db.Column(db.String)
    is_union_member = db.Column(db.Boolean)
    resign_date = db.Column(db.String)
    pagibig_additional = db.Column(db.Float)
    is_pagibig_max = db.Column(db.Boolean)
    rate_min = db.Column(db.Float)
    rate_hour = db.Column(db.Float)
    rate_day = db.Column(db.Float)
    rate_month = db.Column(db.Float)
    timesheet_exempt = db.Column(db.Boolean)
    rank_id = db.Column(db.Integer)
    section_id = db.Column(db.Integer)
    employment_status_id = db.Column(db.Integer)
    job_type_id = db.Column(db.Integer)
    level_id = db.Column(db.Integer)
    position = db.Column(db.String)
    pay_type = db.Column(db.String)
    pay_code = db.Column(db.String)
    gl_account = db.Column(db.String)
    supervisor = db.Column(db.String)
    ndiff1_rate = db.Column(db.Float)
    ndiff2_rate = db.Column(db.Float)
    ot_rate = db.Column(db.Float)
    tardy_rate = db.Column(db.Float)
    ut_rate = db.Column(db.Float)
    absent_rate = db.Column(db.Float)
    income_out = db.Column(db.Float)
    cola_rate = db.Column(db.Float)
    tax_table = db.Column(db.String)
    tax_unit = db.Column(db.String)
    tax_method = db.Column(db.String)
    filed_date = db.Column(db.String)
    approved_by = db.Column(db.String)
    is_suspended = db.Column(db.Boolean)
    suspend_date = db.Column(db.String)
    percentage = db.Column(db.Float)
    evaluator = db.Column(db.String)
    evaluation_date = db.Column(db.String)
    old_rate = db.Column(db.Float)
    old_position = db.Column(db.String)
    old_civil_status = db.Column(db.String)
    email = db.Column(db.String)
    is_inc_alpha = db.Column(db.Boolean)
    is_mwe = db.Column(db.Boolean)
    no_period = db.Column(db.Integer)
    dratemonth = db.Column(db.Float)

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
        return [marshal(r, employee_fields) for r in client_session.query(cls).all()]

    @classmethod
    def get_all_ids(cls, client_db):
        client_session = get_client_session(client_db)
        return [marshal(r, employee_id_fields) for r in client_session.query(cls).all()]

    @classmethod
    def get_by_filter(cls, client_db, **kwargs):
        client_session = get_client_session(client_db)
        return client_session.query(cls).filter_by(**kwargs).first(), client_session

    @classmethod
    def get_reference(cls):
        return marshal(cls.query.first(), employee_fields)

    @classmethod
    def get_all_basic_infos(cls, client_db):
        client_session = get_client_session(client_db)
        return [marshal(r, basic_info_fields) for r in client_session.query(cls).all()]

    @classmethod
    def getEmployees(cls):
        def to_json(x):
            return {
                'id': x.id,
                'employee_number': x.employee_number,
                'firstname': x.firstname,
                'middlename': x.middlename,
                'lastname': x.lastname
            }
        return {'employees': list(map(lambda x: to_json(x), EmployeeModel.query.all()))}
        """return [
            {
                'employee_id': '12345',
                'firstname': 'Juan',
                'middlename': 'Tams',
                'lastname': 'Dela Cruz',
                'gender': 'Male'
            },
            {
                'employee_id': '67891',
                'firstname': 'Mary',
                'middlename': 'Tray',
                'lastname': 'Phautz',
                'gender': 'Female'
            },
        ]"""

    @classmethod
    def getEmployeeDetails(cls, employee_id):
        return {
            'employee_id': '12345',
            'firstname': 'Juan',
            'middlename': 'Tams',
            'lastname': 'Dela Cruz',
            'gender': 'Male'
        }
