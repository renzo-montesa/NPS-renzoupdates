from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


csv_map_fields = {
    'id': mfields.Integer,
    'header': mfields.String,
    'raw_code': mfields.String
}


class CsvMapModel(db.Model):
    __tablename__ = 'csv_map'

    id = db.Column(db.Integer, primary_key = True)
    header = db.Column(db.String)
    raw_code = db.Column(db.String)

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
        records = client_session.query(cls).all()
        client_session.close()
        return [marshal(r, csv_map_fields) for r in records]
