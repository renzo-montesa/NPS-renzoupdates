from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


table_fields = {
    'id': mfields.Integer,
    'branch_id': mfields.Integer,
    'tablename': mfields.String,
    'field': mfields.String,
    'is_req_new': mfields.Boolean,
    'is_req_exist': mfields.Boolean,
    'condition': mfields.String,
    'auto_replace': mfields.String,
    'data_type': mfields.String,
    'valid_length': mfields.Integer
}


class FieldValidatorModel(db.Model):
    __tablename__ = 'field_validator'

    id = db.Column(db.Integer, primary_key = True)
    branch_id = db.Column(db.Integer)
    tablename = db.Column(db.String)
    field = db.Column(db.String)
    is_req_new = db.Column(db.Boolean)
    is_req_exist = db.Column(db.Boolean)
    condition = db.Column(db.String)
    auto_replace = db.Column(db.String)
    data_type = db.Column(db.String)
    valid_length = db.Column(db.Integer)

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
