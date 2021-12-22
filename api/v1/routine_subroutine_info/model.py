from extensions import db


class RoutineSubroutineInfoModel(db.Model):
    __tablename__ = 'routine_subroutine_info'

    id = db.Column(db.Integer, primary_key = True)
    routine_id = db.Column(db.Integer)
    routine_name = db.Column(db.String(150))
    subroutine_id = db.Column(db.Integer)
    subroutine_name = db.Column(db.String(150))
    subroutine_description = db.Column(db.Text)
    max_per_batch = db.Column(db.Integer)
    batch_base = db.Column(db.String(50))
    subroutine_order = db.Column(db.Integer)

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
                'routine_id': x.routine_id,
                'routine_name': x.routine_name,
                'subroutine_id': x.subroutine_id,
                'subroutine_name': x.subroutine_name,
                'subroutine_description': x.subroutine_description,
                'max_per_batch': x.max_per_batch,
                'batch_base': x. batch_base
            }
        return list(map(lambda x: to_json(x), RoutineSubroutineInfoModel.query.all()))

    @classmethod
    def get_by_routine(cls, routine_id):
        def to_json(x):
            return {
                'id': x.id,
                'routine_id': x.routine_id,
                'routine_name': x.routine_name,
                'subroutine_id': x.subroutine_id,
                'subroutine_name': x.subroutine_name,
                'subroutine_description': x.subroutine_description,
                'max_per_batch': x.max_per_batch,
                'batch_base': x. batch_base
            }
        return list(map(lambda x: to_json(x), RoutineSubroutineInfoModel.query.filter_by(routine_id = routine_id).all()))
    
    @classmethod
    def get_subroutines_by_routine(cls, routine_id):
        def to_json(x):
            return {
                'subroutine_id': x.subroutine_id,
                'subroutine_name': x.subroutine_name,
                'subroutine_description': x.subroutine_description,
                'max_per_batch': x.max_per_batch,
                'batch_base': x. batch_base,
                'subroutine_order': x. subroutine_order
            }
        return list(map(lambda x: to_json(x), RoutineSubroutineInfoModel.query.filter_by(routine_id = routine_id).order_by(cls.subroutine_order.asc()).all()))
