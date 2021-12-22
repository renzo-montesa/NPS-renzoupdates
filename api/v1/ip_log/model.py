from extensions import db


class IpLogModel(db.Model):
    __tablename__ = 'ip_log'

    id = db.Column(db.Integer, primary_key = True)
    ip_address = db.Column(db.String(15))
    country = db.Column(db.String(100))
    region = db.Column(db.String(100))
    city = db.Column(db.String(50))
    zip = db.Column(db.String(6))
    latitude = db.Column(db.Numeric(10,6))
    longitude = db.Column(db.Numeric(10,6))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()
