from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


csv_field_fields = {
    'id': mfields.Integer,
    'raw_code': mfields.String,
    'code': mfields.String,
    'formula': mfields.String,
    'tablename': mfields.String,
    't_code': mfields.String
}


class MasterfileCsvFieldModel(db.Model):
    __tablename__ = 'masterfile_csv_field'

    id = db.Column(db.Integer, primary_key = True)
    raw_code = db.Column(db.String)
    code = db.Column(db.String)
    formula = db.Column(db.String)
    tablename = db.Column(db.String)
    t_code = db.Column(db.String)

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
        return [marshal(r, csv_field_fields) for r in client_session.query(cls).all()]
