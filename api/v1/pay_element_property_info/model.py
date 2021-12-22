from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


pay_element_property_info_fields = {
    'id': mfields.Integer,
    'pay_element_code': mfields.String,
    'pay_element_description': mfields.String,
    'pay_element_property': mfields.String,
    'pay_element_value': mfields.String
}


class PayElementPropertyInfoModel(db.Model):
    __tablename__ = 'pay_element_property_info'

    id = db.Column(db.Integer, primary_key=True)
    pay_element_code = db.Column(db.String)
    pay_element_description = db.Column(db.String)
    pay_element_property_id = db.Column(db.Integer, primary_key=True)
    pay_element_property = db.Column(db.String)
    pay_element_value = db.Column(db.String)

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
    def get_pay_element_properties(cls, client_db, id):
        client_session = get_client_session(client_db)
        records = client_session.query(cls).filter_by(id=id).all()
        client_session.close()
        return [marshal(r, pay_element_property_info_fields) for r in records]

