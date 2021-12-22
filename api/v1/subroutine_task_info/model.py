from extensions import db


class SubroutineTaskInfoModel(db.Model):
    __tablename__ = 'subroutine_task_info'

    id = db.Column(db.Integer, primary_key = True)
    subroutine_id = db.Column(db.Integer)
    subroutine_name = db.Column(db.String(150))
    module_id = db.Column(db.Integer)
    package = db.Column(db.String(255))
    class_name = db.Column(db.String(100))
    class_method = db.Column(db.String(100))
    module_description = db.Column(db.Text)
    max_per_batch = db.Column(db.Integer)
    batch_base = db.Column(db.String(50))
    task_order = db.Column(db.Integer)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_tasks_by_subroutine(cls, subroutine_id):
        def to_json(x):
            return {
                'module_id': x.module_id,
                'package': x.package,
                'class_name': x.class_name,
                'class_method': x.class_method,
                'module_description': x.module_description,
                'max_per_batch': x.max_per_batch,
                'batch_base': x.batch_base,
                'task_order': x.task_order
            }
        return {'modules': list(map(lambda x: to_json(x), SubroutineTaskInfoModel.query.filter_by(subroutine_id = subroutine_id).all()))}

