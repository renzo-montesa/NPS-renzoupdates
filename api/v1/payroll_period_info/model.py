from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


table_fields = {
    'id': mfields.Integer,
    'branch_id': mfields.Integer,
    'schedule_id': mfields.Integer,
    'schedule_code': mfields.String,
    'schedule_description': mfields.String,
    'period_start': mfields.String,
    'period_end': mfields.String,
    'transaction_start': mfields.String,
    'transaction_end': mfields.String,
    'is_summarized': mfields.Boolean,
    'is_locked': mfields.Boolean,
    'is_hidden': mfields.Boolean
}


class PayrollPeriodInfoModel(db.Model):
    __tablename__ = 'payroll_period_info'

    id = db.Column(db.Integer, primary_key = True)
    branch_id = db.Column(db.Integer)
    schedule_id = db.Column(db.Integer)
    schedule_code = db.Column(db.String)
    schedule_description = db.Column(db.String)
    period_start = db.Column(db.String)
    period_end = db.Column(db.String)
    transaction_start = db.Column(db.String)
    transaction_end = db.Column(db.String)
    is_summarized = db.Column(db.Boolean)
    is_locked = db.Column(db.Boolean)
    is_hidden = db.Column(db.Boolean)

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
    def get_by_filter(cls, client_db, **kwargs):
        client_session = get_client_session(client_db)
        record = marshal(client_session.query(cls).filter_by(**kwargs).first(), table_fields)
        client_session.close()
        return record
