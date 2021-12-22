from system_core.helper.batch import create_batches


def compute_netpay(data):
    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        data['payslips'][key]['net_pay'] = _compute_netpay(data['payslips'][key])


def _compute_netpay(payslip):
    return round(payslip['gross_pay'] - payslip['other_deductions'] + payslip['nontaxable_earnings'], 2)
