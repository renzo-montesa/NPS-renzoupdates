def get_ytd_pagibig(data):
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

        data['payslips'][key]['ytd']['monthly_pagibig'] = compute_per_month(payslip['historical_payslip_entries'], data['mandatory_codes'][mandatory_code]['pay_element_code'], data['company']['pagibig_max'])
        data['payslips'][key]['ytd'][mandatory_code] = compute_ytd(data['payslips'][key]['ytd']['monthly_pagibig'])


def compute_per_month(payslip_entries, pay_element_code, max_per_month):
    # initialize array
    totals = {}

    for payslip_entry in payslip_entries:
        if payslip_entry['pay_element_code'] == pay_element_code:
            # extract month
            if payslip_entry['period_start'] is None:
                continue

            if len(payslip_entry['period_start']) != 10:
                continue

            period_month = payslip_entry['period_start'][5:7]

            if period_month not in totals:
                totals[period_month] = 0.00

            totals[period_month] += payslip_entry['amount']
            totals[period_month] = min(totals[period_month], max_per_month)

    return totals


def compute_ytd(monthly_pagibig):
    ytd_pagibig = 0.00

    for month in monthly_pagibig:
        ytd_pagibig += monthly_pagibig[month]

    return ytd_pagibig
