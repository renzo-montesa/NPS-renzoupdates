def compute_timekeeping_standard(data, tk_element_code, rate_code):
    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        payslip = data['payslips'][key]
        if not 'payslip_entries' in payslip:
            data['payslips'][key]['payslip_entries'] = {}

        if key not in data['employees']:
            continue

        if tk_element_code in payslip['timekeepings']:
            pay_element_code = payslip['timekeepings'][tk_element_code]['pay_element_code']
            payslip_entry = {
                'pay_element_id': payslip['timekeepings'][tk_element_code]['pay_element_id'],
                'pay_element_code': pay_element_code,
                'amount': 0.00
            }

            percentage = payslip['timekeepings'][tk_element_code]['percentage'] if payslip['timekeepings'][tk_element_code]['percentage'] else 0
            payslip_entry['amount'] = round(payslip['timekeepings'][tk_element_code]['hours'] * \
                percentage * \
                data['employees'][key][rate_code], 2)

            data['payslips'][key]['payslip_entries'][pay_element_code] = payslip_entry
