from extensions import db


class ClientModel(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(254), nullable = False)
    db_name = db.Column(db.String(50), nullable = False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()

    def close(self):
        db.session.close()

    @classmethod
    def get_all(cls):
        def to_json(x):
            return {
                'name': x.name,
                'db_name': x.db_name
            }
        return {'clients': list(map(lambda x: to_json(x), ClientModel.query.all()))}

    @classmethod
    def get_clients_array(cls):
        return list(map(lambda x: x.db_name, ClientModel.query.all()))
