from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


recurring_element_fields = {
    'id': mfields.Integer,
    'employee_id': mfields.Integer,
    'employee_number': mfields.String,
    'pay_element_id': mfields.Integer,
    'pay_element_code': mfields.String,
    'schedule_id': mfields.Integer,
    'schedule_code': mfields.String,
    'amount': mfields.Float,
    'is_active': mfields.Boolean,
    'start_date': mfields.String,
    'end_date': mfields.String,
    'remarks': mfields.String
}


class RecurringElementModel(db.Model):
    __tablename__ = 'recurring_element'

    id = db.Column(db.Integer, primary_key = True)
    employee_id = db.Column(db.Integer)
    employee_number = ""
    pay_element_id = db.Column(db.Integer)
    pay_element_code = ""
    schedule_id = db.Column(db.Integer)
    schedule_code = ""
    amount = db.Column(db.Numeric(14,2))
    is_active = db.Column(db.Boolean)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    remarks = db.Column(db.String)

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
        return [marshal(r, recurring_element_fields) for r in client_session.query(cls).all()]

    @classmethod
    def get_by_filter(cls, client_db, **kwargs):
        client_session = get_client_session(client_db)
        return client_session.query(cls).filter_by(**kwargs).first(), client_session
