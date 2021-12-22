from extensions import db


class ActivityLogModel(db.Model):
    __tablename__ = 'activity_log'

    id = db.Column(db.Integer, primary_key = True)
    ip = db.Column(db.String(15), nullable = False)
    route = db.Column(db.String(250), nullable = False)
    jti = db.Column(db.String(40))
    username = db.Column(db.String(50))
    data = db.Column(db.Text)
    remarks = db.Column(db.String(100))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        def to_json(x):
            return {
                'ip': x.ip,
                'route': x.route,
                'jti': x.jti,
                'username': x.username,
                'data': x.data,
                'remarks': x.remarks
            }
        return {'activity_logs': list(map(lambda x: to_json(x), ActivityLogModel.query.all()))}
