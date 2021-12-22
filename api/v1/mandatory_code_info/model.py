from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


mandatory_code_info_fields = {
    'id': mfields.Integer,
    'pay_element_id': mfields.Integer,
    'pay_element_code': mfields.String,
    'mandatory_code': mfields.String,
    'mandatory_description': mfields.String
}


class MandatoryCodeInfoModel(db.Model):
    __tablename__ = 'mandatory_code_info'

    id = db.Column(db.Integer, primary_key = True)
    pay_element_id = db.Column(db.Integer)
    pay_element_code = db.Column(db.String(50))
    mandatory_code = db.Column(db.String(50))
    mandatory_description = db.Column(db.String(100))

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
    def get_mandatory_codes(cls, client_db):
        client_session = get_client_session(client_db)
        return [marshal(r, mandatory_code_info_fields) for r in client_session.query(cls).all()]
