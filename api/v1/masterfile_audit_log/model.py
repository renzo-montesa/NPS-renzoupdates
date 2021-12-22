from extensions import db
from api.v1.helper.multi_db_management import get_client_session


class MasterfileAuditLogModel(db.Model):
    __tablename__ = 'masterfile_audit_log'

    id = db.Column(db.Integer, primary_key = True)
    employee_number = db.Column(db.String)
    tablename = db.Column(db.String)
    field = db.Column(db.String)
    code = db.Column(db.String)
    old_value = db.Column(db.String)
    new_value = db.Column(db.String)
    transaction_type = db.Column(db.String)
    username = db.Column(db.String)

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