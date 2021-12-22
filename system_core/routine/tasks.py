from extensions import celery
from celery_worker import logger
from pydoc import locate
from api.v1.routine_subroutine_info.model import RoutineSubroutineInfoModel
from api.v1.subroutine_task_info.model import SubroutineTaskInfoModel
from api.v1.process_log.model import ProcessLogModel
from system_core.helper.batch import create_batches


@celery.task(bind=True)
def execute(self, routine_id, client_db, payroll_period_id):
    data = {
        'client_db': client_db,
        'payroll_period_id': payroll_period_id,
        'task': {
            'id': self.request.id,
            'user_id': 1,
            'branch_id': 1,
            'routine_id': routine_id,
            'subroutine_id': 0,
            'task_order': 1
        },
        'subroutine_batch': {
            'max_per_batch': 0,
            'current_batch': 0,
            'batch_base': '',
            'batch_keys': []
        },
        'module_batch': {
            'max_per_batch': 0,
            'current_batch': 0,
            'batch_base': '',
            'batch_keys': []
        }
    }

    routine_process_log = ProcessLogModel.get_process_log_by_task_id(self.request.id)
    if routine_process_log is None:
        routine_process_log = ProcessLogModel(task_id=self.request.id, user_id=1, branch_id=1, routine_id=routine_id, status='In Progress', task_order=data['task']['task_order'])
    else:
        routine_process_log.status = 'In Progress'
    routine_process_log.save_to_db()
    data['task']['task_order'] += 1
    
    subroutines = RoutineSubroutineInfoModel.get_subroutines_by_routine(routine_id)

    for subroutine in subroutines:
        modules = SubroutineTaskInfoModel.get_tasks_by_subroutine(subroutine['subroutine_id'])

        data['task']['subroutine_id'] = subroutine['subroutine_id']
        data['subroutine_batch'] = {
            'max_per_batch': subroutine['max_per_batch'],
            'current_batch': 0,
            'batch_base': subroutine['batch_base'],
            'batch_keys': []
        }

        if not subroutine['batch_base'] is None:
            max_per_batch = data['subroutine_batch']['max_per_batch'] if data['subroutine_batch']['max_per_batch'] > 0 else 999999999
            data['subroutine_batch']['batch_keys'] = create_batches(data[subroutine['batch_base']], max_per_batch)
        else:
            data['subroutine_batch']['batch_keys'] = [[]]

        if subroutine['max_per_batch'] > 0:
            for x in range(len(data['subroutine_batch']['batch_keys'])):
                run_modules(modules['modules'], data)
                data['subroutine_batch']['current_batch'] = x + 1
        else:
            run_modules(modules['modules'], data)
    
    routine_process_log.status = 'Completed'
    routine_process_log.commit_to_db()

    return


def run_modules(modules, data):
    subroutine_process_log = ProcessLogModel(
        task_id=data['task']['id'],
        user_id=data['task']['user_id'],
        branch_id=data['task']['branch_id'],
        routine_id=data['task']['routine_id'],
        subroutine_id=data['task']['subroutine_id'],
        subroutine_batch_no=data['subroutine_batch']['current_batch'],
        status='In Progress',
        task_order=data['task']['task_order']
    )
    subroutine_process_log.save_to_db()
    data['task']['task_order'] += 1

    for module in modules:
        classname = ''
        if not module['class_name'] is None:
            classname = ('.' + module['class_name'])
        my_class = locate(module['package'] + classname)

        data['module_batch'] = {
            'max_per_batch': module['max_per_batch'],
            'current_batch': 0,
            'batch_base': module['batch_base'],
            'batch_keys': []
        }

        batch_keys = data['subroutine_batch']['batch_keys'][data['subroutine_batch']['current_batch']]
    
        if data['module_batch']['max_per_batch'] > 0:
            data['module_batch']['batch_keys'] = create_batches(batch_keys, data['module_batch']['max_per_batch'])
            for x in range(len(data['module_batch']['batch_keys'])):
                module_process_log = ProcessLogModel(
                    task_id=data['task']['id'],
                    user_id=data['task']['user_id'],
                    branch_id=data['task']['branch_id'],
                    routine_id=data['task']['routine_id'],
                    subroutine_id=data['task']['subroutine_id'],
                    subroutine_batch_no=data['subroutine_batch']['current_batch'],
                    module_id=module['module_id'],
                    module_batch_no=data['module_batch']['current_batch'],
                    status='In Progress',
                    task_order=data['task']['task_order']
                )
                module_process_log.save_to_db()
                data['task']['task_order'] += 1

                getattr(my_class, module['class_method'])(data)
                data['module_batch']['current_batch'] = x + 1

                module_process_log.status = 'Completed'
                module_process_log.commit_to_db()
        else:
            module_process_log = ProcessLogModel(
                task_id=data['task']['id'],
                user_id=data['task']['user_id'],
                branch_id=data['task']['branch_id'],
                routine_id=data['task']['routine_id'],
                subroutine_id=data['task']['subroutine_id'],
                subroutine_batch_no=data['subroutine_batch']['current_batch'],
                module_id=module['module_id'],
                module_batch_no=data['module_batch']['current_batch'],
                status='In Progress',
                task_order=data['task']['task_order']
            )
            module_process_log.save_to_db()
            data['task']['task_order'] += 1

            data['module_batch']['batch_keys'] = [batch_keys]
            getattr(my_class, module['class_method'])(data)

            module_process_log.status = 'Completed'
            module_process_log.commit_to_db()
    
    subroutine_process_log.status = 'Completed'
    subroutine_process_log.commit_to_db()
