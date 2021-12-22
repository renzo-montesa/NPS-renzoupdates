from extensions import db
from flask_restful import marshal, fields as mfields


tax_table_info_fields = {
    'id': mfields.Integer,
    'tax_period_id': mfields.Integer,
    'tax_period_code': mfields.String,
    'tax_unit_id': mfields.Integer,
    'tax_unit_code': mfields.String,
    'lower_limit': mfields.Float,
    'upper_limit': mfields.Float,
    'fixed_amount': mfields.Float,
    'percentage': mfields.Float
}


class TaxTableInfoModel(db.Model):
    __tablename__ = 'tax_table_info'

    id = db.Column(db.Integer, primary_key = True)
    tax_period_id = db.Column(db.Integer)
    tax_period_code = db.Column(db.String)
    tax_unit_id = db.Column(db.Integer)
    tax_unit_code = db.Column(db.String)
    lower_limit = db.Column(db.Numeric(14,2))
    upper_limit = db.Column(db.Numeric(14,2))
    fixed_amount = db.Column(db.Numeric(14,2))
    percentage = db.Column(db.Numeric(14,2))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_tax_table_info(cls):
        tax_table_info = cls.query.all()
        return [marshal(r, tax_table_info_fields) for r in tax_table_info]
    
    @classmethod
    def get_tax_table_info_row_by_filter(cls, tax_period_code, tax_unit_code, tax_basis):
        tax_table_info_row = cls.query.filter(cls.tax_period_code==tax_period_code, cls.tax_unit_code==tax_unit_code, cls.upper_limit >= tax_basis, cls.lower_limit <= tax_basis).first()
        return marshal(tax_table_info_row, tax_table_info_fields)
