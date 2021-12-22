from api.v1.payslip.model import PayslipModel


def delete_payslips_by_payroll_period(data):
    PayslipModel.deleteByPayrollPeriod(data['payroll_period']['id'])