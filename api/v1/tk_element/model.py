from extensions import db


class TkElementModel(db.Model):
    __bind_key__ = 'client_db'
    __tablename__ = 'tk_element'

    id = db.Column(db.Integer, primary_key = True)
    pay_element_id = db.Column(db.Integer)
    tk_element_type_id = db.Column(db.Integer)
    code = db.Column(db.String(50))
    description = db.Column(db.String(100))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()
