from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from system_core.report.generate_active_without_payroll_report import generate_active_without_payroll_report
from system_core.routine.tasks import execute
import sys


task_args = {
    'routine': fields.Int()
}


class RunTask(Resource):
    @use_args(task_args)
    def post(self, args):
        if 'routine' in args:
            print(args['routine'], file=sys.stderr)
            result = execute.apply_async(args=[args['routine']])
            return {'task_id': result.id}
            
        return {'task_id': None}
