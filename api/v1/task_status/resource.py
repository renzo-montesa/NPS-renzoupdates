from flask_restful import Resource, marshal, fields as mfields
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from api.v1.user_role_permission_info.model import UserRolePermissionInfoModel, permission_required
from api.v1.process_log_info.model import ProcessLogInfoModel
from api.v1.process_log.model import ProcessLogModel
from api.v1.routine.model import RoutineModel
from api.v1.routine_subroutine_info.model import RoutineSubroutineInfoModel


GET_TASK = 'get_task'
ADD_TASK = 'add_task'
EDIT_TASK = 'edit_task'
DELETE_TASK = 'delete_task'


task_args = {
    'task_id': fields.Str()
}

task_fields = {
    'id': mfields.Integer,
    'task_id': mfields.String,
    'user_id': mfields.Integer,
    'branch_id': mfields.Integer,
    'routine_id': mfields.Integer,
    'subroutine_id': mfields.Integer,
    'subroutine_batch_no': mfields.Integer,
    'module_id': mfields.Integer,
    'module_batch_no': mfields.Integer,
    'status': mfields.String
}

routine_fields = {
    'id': mfields.Integer,
    'name': mfields.String,
    'description': mfields.String,
    'status': mfields.String
}

subroutine_fields = {
    'subroutine_id': mfields.Integer,
    'subroutine_name': mfields.String,
    'subroutine_description': mfields.String,
    'max_per_batch': mfields.Integer,
    'batch_base': mfields.String,
    'subroutine_order': mfields.Integer,
    'status': mfields.String
}

task_list_fields = {
    'tasks': mfields.List(mfields.Nested(task_fields)),
    'routine': mfields.Nested(routine_fields),
    'subroutines': mfields.List(mfields.Nested(subroutine_fields))
}


class TaskStatus(Resource):
    @jwt_required
    @permission_required(GET_TASK)
    @use_args(task_args)
    def get(self, args, task_id=None):
        if 'task_id' in args:
            tasks = ProcessLogInfoModel.query.filter_by(task_id=args['task_id']).all()
            routine = None
            subroutines = None

            if tasks:
                routine = marshal(RoutineModel.get_by_id(tasks[0].routine_id), routine_fields)
                routine_status = ProcessLogModel.get_status_by_task_id(args['task_id'])
                if routine_status:
                    routine['status'] = routine_status.status
                else:
                    routine['status'] = 'On Queue'

                subroutines = [marshal(r, subroutine_fields) for r in RoutineSubroutineInfoModel.get_subroutines_by_routine(tasks[0].routine_id)]

                for index in range(len(subroutines)):
                    task_status = ProcessLogModel.get_status_by_task_id_and_subroutine_id(args['task_id'], subroutines[index]['subroutine_id'])

                    if task_status:
                        subroutines[index]['status'] = task_status.status
                    else:
                        subroutines[index]['status'] = 'On Queue'

            return marshal({
                'tasks': [marshal(r, task_fields) for r in tasks] if tasks else None,
                'routine': routine,
                'subroutines': subroutines,
            }, task_list_fields)
        else:
            tasks = ProcessLogInfoModel.query.all()

            return marshal({
                'tasks': [marshal(r, task_fields) for r in tasks],
                'routine': None,
                'subroutines': None
            }, task_list_fields)
