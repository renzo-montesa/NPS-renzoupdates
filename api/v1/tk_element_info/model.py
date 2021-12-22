from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


table_fields = {
    'id': mfields.Integer,
    'tk_element_code': mfields.String,
    'tk_element_description': mfields.String,
    'tk_element_type_code': mfields.String
}


class TkElementInfoModel(db.Model):
    __bind_key__ = 'client_db'
    __tablename__ = 'tk_element_info'

    id = db.Column(db.Integer, primary_key = True)
    tk_element_code = db.Column(db.String)
    tk_element_description = db.Column(db.String)
    tk_element_type_code = db.Column(db.String)

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
    
    @classmethod
    def get_tk_elements(cls, client_db):
        client_session = get_client_session(client_db)
        return [marshal(r, table_fields) for r in client_session.query(cls).all()]

    @classmethod
    def get_by_filter(cls, client_db, **kwargs):
        client_session = get_client_session(client_db)
        records = client_session.query(cls).filter_by(**kwargs).all()
        client_session.close()
        return [marshal(r, table_fields) for r in records]
