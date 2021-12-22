from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


table_fields = {
    'id': mfields.Integer,
    'employee_id': mfields.Integer,
    'employee_number': mfields.String,
    'tdefa_reg_hrs': mfields.Float,
    'tdefa_nd1': mfields.Float,
    'tdefa_nd2': mfields.Float,
    'tdefa_ot': mfields.Float,
    'tdefa8_ot': mfields.Float,
    'tdefa_nd1_ot': mfields.Float,
    'tdefa_nd18_ot': mfields.Float,
    'tdefa_nd2_ot': mfields.Float,
    'tdefa_nd28_ot': mfields.Float,
    'defa_reg_hrs': mfields.Float,
    'defa_nd1': mfields.Float,
    'defa_nd2': mfields.Float,
    'defa_ot': mfields.Float,
    'defa8_ot': mfields.Float,
    'defa_nd1_ot': mfields.Float,
    'defa_nd18_ot': mfields.Float,
    'defa_nd2_ot': mfields.Float,
    'defa_nd28_ot': mfields.Float,
    'tardy_exempt': mfields.String,
    'ut_exempt': mfields.String,
    'absent_exempt': mfields.String,
    'nd1_exempt': mfields.String,
    'nd2_exempt': mfields.String,
    'ot_exempt': mfields.String,
    'nd1_ot_exempt': mfields.String,
    'nd2_ot_exempt': mfields.String
}


class EmployeeTimekeepingModel(db.Model):
    __tablename__ = 'employee_timekeeping'

    id = db.Column(db.Integer, primary_key = True)
    employee_id = db.Column(db.Integer)
    employee_number = ""
    tdefa_reg_hrs = db.Column(db.Float)
    tdefa_nd1 = db.Column(db.Float)
    tdefa_nd2 = db.Column(db.Float)
    tdefa_ot = db.Column(db.Float)
    tdefa8_ot = db.Column(db.Float)
    tdefa_nd1_ot = db.Column(db.Float)
    tdefa_nd18_ot = db.Column(db.Float)
    tdefa_nd2_ot = db.Column(db.Float)
    tdefa_nd28_ot = db.Column(db.Float)
    defa_reg_hrs = db.Column(db.Float)
    defa_nd1 = db.Column(db.Float)
    defa_nd2 = db.Column(db.Float)
    defa_ot = db.Column(db.Float)
    defa8_ot = db.Column(db.Float)
    defa_nd1_ot = db.Column(db.Float)
    defa_nd18_ot = db.Column(db.Float)
    defa_nd2_ot = db.Column(db.Float)
    defa_nd28_ot = db.Column(db.Float)
    tardy_exempt = db.Column(db.String)
    ut_exempt = db.Column(db.String)
    absent_exempt = db.Column(db.String)
    nd1_exempt = db.Column(db.String)
    nd2_exempt = db.Column(db.String)
    ot_exempt = db.Column(db.String)
    nd1_ot_exempt = db.Column(db.String)
    nd2_ot_exempt = db.Column(db.String)

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
