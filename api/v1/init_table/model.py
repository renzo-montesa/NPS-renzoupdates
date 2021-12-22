from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


init_table_fields = {
    'id': mfields.Integer,
    'tablename': mfields.String,
    'index_field': mfields.String,
    'filter': mfields.String
}


class InitTableModel(db.Model):
    __tablename__ = 'init_table'

    id = db.Column(db.Integer, primary_key = True)
    tablename = db.Column(db.String)
    index_field = db.Column(db.String)
    filter = db.Column(db.String)

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
        return [marshal(r, init_table_fields) for r in records]
