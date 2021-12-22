from extensions import db
from flask_restful import marshal, fields as mfields


med_table_fields = {
    'id': mfields.Integer,
    'lower_limit': mfields.Float,
    'upper_limit': mfields.Float,
    'empl_share': mfields.Float,
    'empr_share': mfields.Float,
    'percentage': mfields.Float
}


class MedTableModel(db.Model):
    __tablename__ = 'med_table'

    id = db.Column(db.Integer, primary_key = True)
    lower_limit = db.Column(db.Numeric(14,2))
    upper_limit = db.Column(db.Numeric(14,2))
    empl_share = db.Column(db.Numeric(14,2))
    empr_share = db.Column(db.Numeric(14,2))
    percentage = db.Column(db.Numeric(6,4))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_med_table(cls):
        med_table = cls.query.all()
        return [marshal(r, med_table_fields) for r in med_table]
    
    @classmethod
    def get_med_row_by_basis(cls, med_basis):
        med_row = cls.query.filter(cls.upper_limit >= med_basis, cls.lower_limit <= med_basis).first()
        return marshal(med_row, med_table_fields)
