from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


schedule_fields = {
    'id': mfields.Integer,
    'code': mfields.String,
    'description': mfields.String
}


class ScheduleModel(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.String(10))
    description = db.Column(db.String(100))

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
        return [marshal(r, schedule_fields) for r in client_session.query(cls).all()]
