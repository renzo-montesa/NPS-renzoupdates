from api.v1.payslip.model import PayslipModel
from system_core.helper.array_to_dict import (array_to_dict_by_key)


def get_payslips_by_payroll_period(data):
    data['payslips'] = array_to_dict_by_key(PayslipModel.getPayslipsByPayrollPeriodId(data['client_db'], data['payroll_period']['id']), 'employee_id')
