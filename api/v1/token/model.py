from extensions import db


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_token'

    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)


class WhitelistedTokenModel(db.Model):
    __tablename__ = 'whitelisted_token'

    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    expiry_date = db.Column(db.String)

    def add(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def is_jti_whitelisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)
