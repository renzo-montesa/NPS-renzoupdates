"""
Get the total earnings included in med basis
"""
def get_current_include(data):
    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        payslip = data['payslips'][key]
        if not 'mandatories' in payslip:
            data['payslips'][key]['mandatories'] = {}

        if key not in data['employees']:
            continue
        
        if not 'med' in data['payslips'][key]['mandatories']:
            data['payslips'][key]['mandatories']['med'] = {
                'mandatory_code': 'med',
                'basis': 0.00,
                'include_basis': 0.00,
                'employee_share': 0.00,
                'employer_share': 0.00
            }
        
        if not 'payslip_entries' in payslip:
            data['payslips'][key]['payslip_entries'] = {}
            continue

        for entry_key, payslip_entry in payslip['payslip_entries'].items():
            if entry_key in data['pay_elements']:
                if 'is_inc_med' not in data['pay_elements'][entry_key]:
                    continue

                if data['pay_elements'][entry_key]['is_inc_med'] != 'TRUE':
                    continue

                if data['employees'][key]['med_basis'] == "G":
                    if 'is_taxable' in data['pay_elements'][entry_key]:
                        if data['pay_elements'][entry_key]['is_taxable'] == 'TRUE':
                            continue
                    
                data['payslips'][key]['mandatories']['med']['include_basis'] += (payslip_entry['amount'] * data['pay_elements'][entry_key]['multiplier'])
                    
