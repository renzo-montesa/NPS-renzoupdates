from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


pay_element_fields = {
    'id': mfields.Integer,
    'pay_element_type_id': mfields.Integer,
    'code': mfields.String,
    'description': mfields.String,
    'multiplier': mfields.Float
}


class PayElementModel(db.Model):
    __bind_key__ = 'client_db'
    __tablename__ = 'pay_element'

    id = db.Column(db.Integer, primary_key = True)
    pay_element_type_id = db.Column(db.Integer)
    code = db.Column(db.String(50))
    description = db.Column(db.String(100))
    multiplier = db.Column(db.Numeric(6,4))

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
        return [marshal(r, pay_element_fields) for r in client_session.query(cls).all()]
    
    @classmethod
    def get_pay_elements(cls):
        pay_elements = cls.query.all()
        return [marshal(r, pay_element_fields) for r in pay_elements]

    @classmethod
    def get_by_filter(cls, client_db, **kwargs):
        client_session = get_client_session(client_db)
        return client_session.query(cls).filter_by(**kwargs).first(), client_session
