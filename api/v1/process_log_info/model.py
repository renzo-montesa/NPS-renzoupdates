from extensions import db
from flask_restful import marshal, fields as mfields


process_log_fields = {
    'id': mfields.Integer,
    'task_id': mfields.String,
    'user_id': mfields.Integer,
    'branch_id': mfields.Integer,
    'routine_id': mfields.Integer,
    'routine_name': mfields.String,
    'subroutine_id': mfields.Integer,
    'subroutine_name': mfields.String,
    'subroutine_batch_no': mfields.Integer,
    'module_id': mfields.Integer,
    'class_method': mfields.String,
    'module_description': mfields.String,
    'module_batch_no': mfields.Integer,
    'task_order': mfields.Integer,
    'status': mfields.String
}


class ProcessLogInfoModel(db.Model):
    __tablename__ = 'process_log_info'

    id = db.Column(db.Integer, primary_key = True)
    task_id = db.Column(db.String(155))
    user_id = db.Column(db.Integer)
    branch_id = db.Column(db.Integer)
    routine_id = db.Column(db.Integer)
    routine_name = db.Column(db.String)
    subroutine_id = db.Column(db.Integer)
    subroutine_name = db.Column(db.String)
    subroutine_batch_no = db.Column(db.Integer)
    module_id = db.Column(db.Integer)
    class_method = db.Column(db.String)
    module_description = db.Column(db.String)
    module_batch_no = db.Column(db.Integer)
    task_order = db.Column(db.Integer)
    status = db.Column(db.String(50))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_process_logs(cls):
        process_logs = cls.query.all()
        return [marshal(r, process_log_fields) for r in process_logs]

    @classmethod
    def get_process_logs_by_task_id(cls, task_id):
        return [marshal(r, process_log_fields) for r in cls.query.filter_by(task_id=task_id).all()]

