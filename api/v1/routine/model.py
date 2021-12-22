from extensions import db


class RoutineModel(db.Model):
    __tablename__ = 'app_routine'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.Text)

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
                'id': x.id,
                'name': x.name,
                'description': x.description
            }
        return list(map(lambda x: to_json(x), RoutineModel.query.all()))

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
