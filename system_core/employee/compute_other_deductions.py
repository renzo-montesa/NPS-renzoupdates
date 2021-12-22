def compute_other_deductions(data):
    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        payslip = data['payslips'][key]
        data['payslips'][key]['other_deductions'] = 0.00

        if not 'payslip_entries' in payslip:
            data['payslips'][key]['payslip_entries'] = {}
            continue

        for entry_key, payslip_entry in payslip['payslip_entries'].items():
            if entry_key in data['pay_elements']:
                if data['pay_elements'][entry_key]['pay_element_type_code'] == 'deduction':
                    data['payslips'][key]['other_deductions'] += round((payslip_entry['amount'] * data['pay_elements'][entry_key]['multiplier']), 2)
			
        data['payslips'][key]['other_deductions'] = round(data['payslips'][key]['other_deductions'], 2)
