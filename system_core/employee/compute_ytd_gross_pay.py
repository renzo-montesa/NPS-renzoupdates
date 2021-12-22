def compute_ytd_gross_pay(data):
    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        payslip = data['payslips'][key]

        if not 'ytd' in data['payslips'][key]:
            data['payslips'][key]['ytd'] = {}
        
        if not 'gross_pay' in data['payslips'][key]['ytd']:
            data['payslips'][key]['ytd']['gross_pay'] = 0.00

        if not 'historical_payslip_entries' in data['payslips'][key]:
            continue

        for payslip_entry in payslip['historical_payslip_entries']:
            if payslip_entry['pay_element_code'] in data['pay_elements']:
                if 'is_taxable' in data['pay_elements'][payslip_entry['pay_element_code']]:
                    if data['pay_elements'][payslip_entry['pay_element_code']]['is_taxable'] == 'TRUE':
                        data['payslips'][key]['ytd']['gross_pay'] += payslip_entry['amount']