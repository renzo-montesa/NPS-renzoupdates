from extensions import db


class PermissionModel(db.Model):
    __tablename__ = 'permission'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)

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
                'name': x.name
            }
        return {'permissions': list(map(lambda x: to_json(x), PermissionModel.query.all()))}
