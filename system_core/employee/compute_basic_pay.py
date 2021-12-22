def compute_basic_pay(data):
    tk_element_code = "reg_hrs"

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

            if data['employees'][key]['pay_type'] == "M" and data['employees'][key]['pay_code'] != "B":
                payslip_entry['amount'] = compute_basic_pay_monthly(data['employees'][key], payslip)
            elif data['employees'][key]['pay_type'] == "M" and data['employees'][key]['pay_code'] == "B":
                payslip_entry['amount'] = compute_basic_pay_monthly_paycode_b(data['employees'][key]['rate_month'], payslip['timekeepings'][tk_element_code]['hours'])
            else:
                payslip_entry['amount'] = compute_basic_pay_daily(data['employees'][key], payslip)

            data['payslips'][key]['payslip_entries'][pay_element_code] = payslip_entry

def compute_basic_pay_daily(employee, payslip):
    basic_pay = 0.00

    if employee['pay_type'] == "D":
        basic_pay = round(payslip['timekeepings']['reg_hrs']['hours'] * employee['rate_hour'], 2)
    
    return basic_pay

def compute_basic_pay_monthly_paycode_b(rate, hours):
    return round(((((rate * 12) / 260) * hours) / 8), 2)

def compute_basic_pay_monthly(employee, payslip):
    basic_pay = 0.00

    if employee['pay_type'] == "M":
        if employee['pay_code'] == "M":
            basic_pay = round(employee['rate_month'], 2)
        elif employee['pay_code'] == "B":
            basic_pay = round(((employee['rate_month'] * 12) / 260), 2)
        else:
            basic_pay = round(employee['rate_month'] / 2, 2)
    
    return basic_pay
