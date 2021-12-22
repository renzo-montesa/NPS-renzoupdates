from extensions import db
from api.v1.helper.multi_db_management import get_client_session


class LoanCodeModel(db.Model):
    __tablename__ = 'loan_code'

    id = db.Column(db.Integer, primary_key = True)
    pay_element_id = db.Column(db.Integer)
    loan_type_id = db.Column(db.Integer)

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
