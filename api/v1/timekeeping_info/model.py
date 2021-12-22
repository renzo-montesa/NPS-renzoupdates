from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


timekeeping_info_fields = {
    'id': mfields.Integer,
    'payslip_id': mfields.Integer,
    'tk_element_id': mfields.Integer,
    'hours': mfields.Float,
    'payslip_id': mfields.Integer,
    'employee_id': mfields.Integer,
    'branch_id': mfields.Integer,
    'tk_element_code': mfields.String,
    'tk_element_description': mfields.String,
    'tk_element_type_code': mfields.String,
    'percentage': mfields.Float,
    'pay_element_id': mfields.Integer,
    'pay_element_code': mfields.String,
    'formula': mfields.String
}


class TimekeepingInfoModel(db.Model):
    __bind_key__ = 'client_db'
    __tablename__ = 'timekeeping_info'

    id = db.Column(db.Integer, primary_key = True)
    payslip_id = db.Column(db.Integer)
    employee_id = db.Column(db.Integer)
    branch_id = db.Column(db.Integer)
    tk_element_code = db.Column(db.String)
    tk_element_description = db.Column(db.String)
    hours = db.Column(db.Numeric(14,4))
    tk_element_type_code = db.Column(db.String)
    percentage = db.Column(db.Numeric(14,4))
    pay_element_id = db.Column(db.Integer)
    pay_element_code = db.Column(db.String)
    formula = db.Column(db.String)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def get_by_filter(cls, client_db, **kwargs):
        client_session = get_client_session(client_db)
        records = client_session.query(cls).filter_by(**kwargs).all()
        client_session.close()
        return [marshal(r, timekeeping_info_fields) for r in records]
