def get_ytd_mandatory(data, mandatory_code):
    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        payslip = data['payslips'][key]

        if not 'ytd' in data['payslips'][key]:
            data['payslips'][key]['ytd'] = {}
        
        if not mandatory_code in data['payslips'][key]['ytd']:
            data['payslips'][key]['ytd'][mandatory_code] = 0.00

        if not 'historical_payslip_entries' in data['payslips'][key]:
            continue

        if not 'mandatory_codes' in data:
            continue

        if not mandatory_code in data['mandatory_codes']:
            continue

        for payslip_entry in payslip['historical_payslip_entries']:
            if payslip_entry['pay_element_code'] == data['mandatory_codes'][mandatory_code]['pay_element_code']:
                data['payslips'][key]['ytd'][mandatory_code] += payslip_entry['amount']