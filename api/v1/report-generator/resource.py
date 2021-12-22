from flask_restful import Resource
from api.v1.process_log.model import ProcessLogModel
from system_core.routine.tasks import execute
from system_core.report.generate_payroll_report import generate_payroll_report


class Employee(Resource):
    def get(self):
        result = execute.apply_async(args=[1])
        return {'task_id': result.id}

    def post(self):
        #result = execute.apply_async(args=[5])
        #return {'task_id': result.id}
        generate_payroll_report({})
