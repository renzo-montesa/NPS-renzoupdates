from extensions import db
from flask_restful import marshal, fields as mfields


hdmf_table_fields = {
    'id': mfields.Integer,
    'lower_limit': mfields.Float,
    'upper_limit': mfields.Float,
    'empl_percent': mfields.Float,
    'empr_percent': mfields.Float,
    'empl_max': mfields.Float,
    'empr_max': mfields.Float
}


class HdmfTableModel(db.Model):
    __tablename__ = 'hdmf_table'

    id = db.Column(db.Integer, primary_key = True)
    lower_limit = db.Column(db.Numeric(14,2))
    upper_limit = db.Column(db.Numeric(14,2))
    empl_percent = db.Column(db.Numeric(14,2))
    empr_percent = db.Column(db.Numeric(14,2))
    empl_max = db.Column(db.Numeric(14,2))
    empr_max = db.Column(db.Numeric(14,2))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_hdmf_table(cls):
        hdmf_table = cls.query.all()
        return [marshal(r, hdmf_table_fields) for r in hdmf_table]
    
    @classmethod
    def get_hdmf_row_by_basis(cls, hdmf_basis):
        hdmf_row = cls.query.filter(cls.upper_limit >= hdmf_basis, cls.lower_limit <= hdmf_basis).first()
        return marshal(hdmf_row, hdmf_table_fields)
