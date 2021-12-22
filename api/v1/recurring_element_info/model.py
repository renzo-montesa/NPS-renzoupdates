from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


recurring_element_info_fields = {
    'id': mfields.Integer,
    'employee_id': mfields.Integer,
    'schedule_id': mfields.Integer,
    'schedule_code': mfields.String,
    'pay_element_id': mfields.Integer,
    'pay_element_code': mfields.String,
    'pay_element_description': mfields.String,
    'pay_element_type_id': mfields.Integer,
    'pay_element_type_code': mfields.String,
    'amount': mfields.Float,
    'is_active': mfields.Boolean,
    'start_date': mfields.String,
    'end_date': mfields.String
}


class RecurringElementInfoModel(db.Model):
    __bind_key__ = 'client_db'
    __tablename__ = 'recurring_element_info'

    id = db.Column(db.Integer, primary_key = True)
    employee_id = db.Column(db.Integer)
    schedule_id = db.Column(db.Integer)
    schedule_code = db.Column(db.String)
    pay_element_id = db.Column(db.Integer)
    pay_element_code = db.Column(db.String(50))
    pay_element_description = db.Column(db.String(100))
    pay_element_type_id = db.Column(db.Integer)
    pay_element_type_code = db.Column(db.String(50))
    amount = db.Column(db.Numeric(14,2))
    is_active = db.Column(db.Boolean)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_by_period(cls, client_db, period_start):
        client_session = get_client_session(client_db)
        records = client_session.query(cls).filter(cls.start_date <= period_start, cls.end_date >= period_start).all()
        client_session.close()
        return [marshal(r, recurring_element_info_fields) for r in records]
