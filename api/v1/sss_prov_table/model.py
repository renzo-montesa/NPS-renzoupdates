from extensions import db
from flask_restful import marshal, fields as mfields


sss_table_fields = {
    'id': mfields.Integer,
    'lower_limit': mfields.Float,
    'upper_limit': mfields.Float,
    'provident_fund': mfields.Float,
    'employee_share': mfields.Float,
    'employer_share': mfields.Float
}


class SssProvTableModel(db.Model):
    __tablename__ = 'sss_prov_table'

    id = db.Column(db.Integer, primary_key = True)
    lower_limit = db.Column(db.Numeric(14,2))
    upper_limit = db.Column(db.Numeric(14,2))
    provident_fund = db.Column(db.Numeric(14,2))
    employee_share = db.Column(db.Numeric(14,2))
    employer_share = db.Column(db.Numeric(14,2))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_sss_table(cls):
        sss_table = cls.query.all()
        return [marshal(r, sss_table_fields) for r in sss_table]
    
    @classmethod
    def get_sss_row_by_basis(cls, sss_basis):
        sss_row = cls.query.filter(cls.upper_limit >= sss_basis, cls.lower_limit <= sss_basis).first()
        return marshal(sss_row, sss_table_fields)
