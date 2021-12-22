from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


pay_element_info_fields = {
    'id': mfields.Integer,
    'pay_element_type_id': mfields.Integer,
    'pay_element_type_code': mfields.String,
    'pay_element_code': mfields.String,
    'pay_element_description': mfields.String,
    'formula': mfields.String,
    'multiplier': mfields.Float
}


class PayElementInfoModel(db.Model):
    __tablename__ = 'pay_element_info'

    id = db.Column(db.Integer, primary_key = True)
    pay_element_type_id = db.Column(db.Integer)
    pay_element_type_code = db.Column(db.String(50))
    pay_element_code = db.Column(db.String(50))
    pay_element_description = db.Column(db.String(100))
    formula = db.Column(db.String)
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
    def get_pay_elements(cls, client_db):
        client_session = get_client_session(client_db)
        records = client_session.query(cls).all()
        client_session.close()
        return [marshal(r, pay_element_info_fields) for r in records]
