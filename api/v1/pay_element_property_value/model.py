from extensions import db
from api.v1.helper.multi_db_management import get_client_session


class PayElementPropertyValueModel(db.Model):
    __tablename__ = 'pay_element_property_value'

    id = db.Column(db.Integer, primary_key = True)
    pay_element_id = db.Column(db.Integer)
    pay_element_property_id = db.Column(db.Integer)
    value = db.Column(db.String(255))

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
