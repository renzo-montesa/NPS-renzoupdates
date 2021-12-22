from extensions import db
from flask_restful import marshal, fields as mfields
from api.v1.helper.multi_db_management import get_client_session


table_fields = {
    'id': mfields.Integer,
    'employee_id': mfields.Integer,
    'employee_number': mfields.String,
    'company_name': mfields.String,
    'address': mfields.String,
    'telephone': mfields.String,
    'tin': mfields.String,
    'rate': mfields.Float,
    'pytd_taxable_earning': mfields.Float,
    'pytd_nontax_earning': mfields.Float,
    'pytd_nontax_bonus': mfields.Float,
    'pytd_taxable_bonus': mfields.Float,
    'pytd_wtax': mfields.Float,
    'pytd_union': mfields.Float,
    'pytd_sss': mfields.Float,
    'pytd_med': mfields.Float,
    'pytd_pagib': mfields.Float
}


class PreviousEmployerModel(db.Model):
    __tablename__ = 'previous_employer'

    id = db.Column(db.Integer, primary_key = True)
    employee_id = db.Column(db.Integer)
    employee_number = ""
    company_name = db.Column(db.String)
    address = db.Column(db.String)
    telephone = db.Column(db.String)
    tin = db.Column(db.String)
    rate = db.Column(db.Float)
    pytd_taxable_earning = db.Column(db.Float)
    pytd_nontax_earning = db.Column(db.Float)
    pytd_nontax_bonus = db.Column(db.Float)
    pytd_taxable_bonus = db.Column(db.Float)
    pytd_wtax = db.Column(db.Float)
    pytd_union = db.Column(db.Float)
    pytd_sss = db.Column(db.Float)
    pytd_med = db.Column(db.Float)
    pytd_pagib = db.Column(db.Float)

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
        return client_session.query(cls).filter_by(**kwargs).first(), client_session
