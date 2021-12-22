def get_current_pagibig(data):
    mandatory_code = 'pagibig'

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

        if data['payroll_period'] is None:
                continue

        if len(data['payroll_period']['period_start']) != 10:
            continue

        current_month = data['payroll_period']['period_start'][5:7]

        data['payslips'][key]['current_pagibig'] = compute_month(payslip['historical_payslip_entries'], data['mandatory_codes'][mandatory_code]['pay_element_code'], data['company']['pagibig_max'], payslip['mandatories'][mandatory_code]['employee_share'], current_month)


def compute_month(payslip_entries, pay_element_code, max_per_month, employee_share, current_month):
    # initialize array
    total = 0.00

    for payslip_entry in payslip_entries:
        if payslip_entry['pay_element_code'] == pay_element_code:
            # extract month
            if payslip_entry['period_start'] is None:
                continue

            if len(payslip_entry['period_start']) != 10:
                continue

            period_month = payslip_entry['period_start'][5:7]

            if period_month != current_month:
                continue

            total += payslip_entry['amount']
            total = min(total, max_per_month)

    return total