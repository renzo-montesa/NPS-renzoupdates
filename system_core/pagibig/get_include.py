def get_current_include(data):
    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        payslip = data['payslips'][key]
        if not 'mandatories' in payslip:
            data['payslips'][key]['mandatories'] = {}

        if key not in data['employees']:
            continue
        
        if not 'pagibig' in data['payslips'][key]['mandatories']:
            data['payslips'][key]['mandatories']['pagibig'] = {
                'mandatory_code': 'pagibig',
                'basis': 0.00,
                'include_basis': 0.00,
                'employee_share': 0.00,
                'employer_share': 0.00,
                'pagibig_additional': 0.00
            }
        
        if not 'payslip_entries' in payslip:
            data['payslips'][key]['payslip_entries'] = {}
            continue

        for entry_key, payslip_entry in payslip['payslip_entries'].items():
            if entry_key in data['pay_elements']:
                if 'is_inc_pagibig' not in data['pay_elements'][entry_key]:
                    continue

                if data['pay_elements'][entry_key]['is_inc_pagibig'] != 'TRUE':
                    continue
                    
                data['payslips'][key]['mandatories']['pagibig']['include_basis'] += (payslip_entry['amount'] * data['pay_elements'][entry_key]['multiplier'])