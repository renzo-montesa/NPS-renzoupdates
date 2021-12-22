from extensions import db


class TkElementTypeModel(db.Model):
    __bind_key__ = 'client_db'
    __tablename__ = 'tk_element_type'

    id = db.Column(db.Integer, primary_key = True)
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
