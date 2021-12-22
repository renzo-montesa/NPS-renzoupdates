from extensions import db
from flask_restful import marshal, fields as mfields
from system_core.helper.array_to_dict import (array_to_dict_by_key)
from api.v1.helper.multi_db_management import get_client_session


payslip_entry_info_fields = {
    'id': mfields.Integer,
    'payslip_id': mfields.Integer,
    'pay_element_id': mfields.Integer,
    'pay_element_code': mfields.String,
    'amount': mfields.Float
}


class PayslipEntryInfoModel(db.Model):
    __bind_key__ = 'client_db'
    __tablename__ = 'payslip_entry_info'

    id = db.Column(db.Integer, primary_key = True)
    payslip_id = db.Column(db.Integer)
    pay_element_id = db.Column(db.Integer)
    pay_element_code = db.Column(db.String(50))
    amount = db.Column(db.Numeric(14,2))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()
    

    @classmethod
    def get_payslip_entries_by_payslip_id(cls, client_db, payslip_id):
        client_session = get_client_session(client_db)
        records = client_session.query(cls).filter_by(payslip_id=payslip_id).all()
        client_session.close()
        return array_to_dict_by_key([marshal(r, payslip_entry_info_fields) for r in records], 'pay_element_code')
    

    @classmethod
    def get_historical_payslip_entries_by_payslip_id(cls, payslip_id):
        payslip_entries = cls.query.filter(cls.payslip_id!=payslip_id).all()
        return [marshal(r, payslip_entry_info_fields) for r in payslip_entries]
