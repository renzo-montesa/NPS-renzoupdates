def get_tax_basis(data):
    for key, payslip in data['payslips'].items():
        if not 'mandatories' in payslip:
            data['payslips'][key]['mandatories'] = {}
        
        if not 'tax' in data['payslips'][key]['mandatories']:
            data['payslips'][key]['mandatories']['tax'] = {
                'mandatory_code': 'tax',
                'basis': 0.00,
                'employee_share': 0.00
            }
        
        data['payslips'][key]['mandatories']['tax']['basis'] = payslip['gross_pay'] - (payslip['mandatories']['sss']['employee_share'] + payslip['mandatories']['med']['employee_share'] + min(payslip['mandatories']['pagibig']['employee_share'], data['company']['pagibig_max']))
