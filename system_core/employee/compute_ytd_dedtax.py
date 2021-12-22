def compute_ytd_dedtax(data):
    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        payslip = data['payslips'][key]

        if not 'ytd' in data['payslips'][key]:
            data['payslips'][key]['ytd'] = {}
        
        if not 'deductible_tax' in data['payslips'][key]['ytd']:
            data['payslips'][key]['ytd']['deductible_tax'] = 0.00

        if not 'historical_payslip_entries' in data['payslips'][key]:
            continue

        for payslip_entry in payslip['historical_payslip_entries']:
            if payslip_entry['pay_element_code'] not in data['pay_elements']:
                continue

            if 'is_ded_tax' not in data['pay_elements'][payslip_entry['pay_element_code']]:
                continue

            if data['pay_elements'][payslip_entry['pay_element_code']]['is_ded_tax'] == 'TRUE':
                if 'is_health_prem' in data['pay_elements'][payslip_entry['pay_element_code']]:
                    if data['pay_elements'][payslip_entry['pay_element_code']]['is_health_prem'] == 'TRUE':
                        continue

                data['payslips'][key]['ytd']['deductible_tax'] += payslip_entry['amount']