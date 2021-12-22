from api.v1.payroll_period_info.model import PayrollPeriodInfoModel
from flask_restful import marshal, fields as mfields
import sys
from celery.utils.log import get_task_logger
import json


logger = get_task_logger(__name__)


payroll_period_fields = {
    'id': mfields.Integer,
    'branch_id': mfields.Integer,
    'schedule_id': mfields.Integer,
    'schedule_code': mfields.String,
    'schedule_description': mfields.String,
    'period_start': mfields.String,
    'period_end': mfields.String,
    'transaction_start': mfields.String,
    'transaction_end': mfields.String,
    'is_summarized': mfields.Boolean,
    'is_locked': mfields.Boolean,
    'is_hidden': mfields.Boolean
}


def get_payroll_period(data):
    data['payroll_period'] = PayrollPeriodInfoModel.get_by_filter(data['client_db'], id=data['payroll_period_id'])
    logger.info('payroll_period: ' + json.dumps(data['payroll_period']))
