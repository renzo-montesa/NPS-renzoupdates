from extensions import db


class TkElementRateModel(db.Model):
    __bind_key__ = 'client_db'
    __tablename__ = 'tk_element_rate'

    id = db.Column(db.Integer, primary_key = True)
    branch_id = db.Column(db.Integer)
    tk_element_id = db.Column(db.Integer)
    percentage = db.Column(db.Numeric(6,4))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()
