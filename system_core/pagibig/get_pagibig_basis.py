def get_pagibig_basis(data):
    get_basis_normal(data)

def get_basis_normal(data):
    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        payslip = data['payslips'][key]
        if not 'mandatories' in payslip:
            data['payslips'][key]['mandatories'] = {}
        
        if not 'pagibig' in data['payslips'][key]['mandatories']:
            data['payslips'][key]['mandatories']['pagibig'] = {
                'mandatory_code': 'pagibig',
                'basis': 0.00,
                'include_basis': 0.00,
                'employee_share': 0.00,
                'employer_share': 0.00,
                'pagibig_additional': 0.00
            }

        data['payslips'][key]['mandatories']['pagibig']['basis'] = data['payslips'][key]['mandatories']['pagibig']['include_basis']
        
        if not 'payslip_entries' in payslip:
            data['payslips'][key]['payslip_entries'] = {}
            continue

        if 'basic_pay' in payslip['payslip_entries']:
            data['payslips'][key]['mandatories']['pagibig']['basis'] += payslip['payslip_entries']['basic_pay']['amount']

def get_basis_normal_atu(data):
    data['pagibig']['basis'] = data['payslip']['basic_pay'] - (data['payslip']['absences'] + data['payslip']['tardiness'] + data['payslip']['undertime']) + data['payslip']['tot_inc_pagibig'] + data['pagibig']['prev_basic_pay'] - (data['payslip']['prev_absences'] + data['payslip']['prev_tardiness'] + data['payslip']['prev_undertime']) + data['pagibig']['prev_tot_inc_pagibig']
    return data
