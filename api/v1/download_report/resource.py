from flask.helpers import send_from_directory
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
import config


task_args = {
    'routine': fields.Int()
}


class DownloadReport(Resource):
    @use_args(task_args)
    def get(self, args):
        return send_from_directory(directory=config.REPORT_DIR, filename="payroll_report_200101.xlsx")
