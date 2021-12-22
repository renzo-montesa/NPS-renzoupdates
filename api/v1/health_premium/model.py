from extensions import db
from sqlalchemy import text
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


health_premium_fields = {
    'id': mfields.Integer,
    'employee_id': mfields.Integer,
    'amount': mfields.Float,
    'policy_no': mfields.String,
    'year_cover': mfields.Integer
}


class HealthPremiumModel(db.Model):
    __tablename__ = 'health_premium'

    id = db.Column(db.Integer, primary_key = True)
    employee_id = db.Column(db.Integer)
    amount = db.Column(db.Numeric(14,2))
    policy_no = db.Column(db.String)
    year_cover = db.Column(db.Integer)

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
    def get_by_employee_and_year(cls, client_db, employee_id, year_cover):
        client_session = get_client_session(client_db)
        return [marshal(r, health_premium_fields) for r in client_session.query(cls).filter_by(employee_id=employee_id, year_cover=year_cover).all()]


    @classmethod
    def get_total_by_employee_and_year(cls, client_db, employee_id, year_cover):
        client_session = get_client_session(client_db)
        stmt = "SELECT id, employee_id, SUM(amount) AS amount, policy_no, year_cover "
        stmt += "FROM health_premium "
        stmt += "WHERE employee_id=:employee_id AND year_cover=:year_cover "
        result = client_session.query(cls).from_statement(text(stmt)).params(employee_id=employee_id, year_cover=year_cover).first()
        return marshal(result, health_premium_fields)