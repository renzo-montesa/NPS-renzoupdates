from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


class TimekeepingModel(db.Model):
    __tablename__ = 'timekeeping'

    id = db.Column(db.Integer, primary_key = True)
    payslip_id = db.Column(db.Integer)
    tk_element_id = db.Column(db.Integer)
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
    def get_by_filter(cls, client_db, **kwargs):
        client_session = get_client_session(client_db)
        return client_session.query(cls).filter_by(**kwargs).first(), client_session
