import sys

def compute_gross_taxable(data):
    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        payslip = data['payslips'][key]
        if not 'mandatories' in payslip:
            data['payslips'][key]['mandatories'] = {}
        
        if not 'tax' in data['payslips'][key]['mandatories']:
            data['payslips'][key]['mandatories']['tax'] = {
                'mandatory_code': 'tax',
                'basis': 0.00,
                'employee_share': 0.00
            }
        
        data['payslips'][key]['mandatories']['tax']['basis'] = payslip['gross_pay'] - (payslip['mandatories']['sss']['employee_share'] + payslip['mandatories']['med']['employee_share'] + min(payslip['mandatories']['pagibig']['employee_share'], data['company']['pagibig_max']) + payslip['mandatories']['pagibig']['pagibig_additional'])
