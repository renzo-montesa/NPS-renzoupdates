def pagibig_normal(data):
    data['pagibig']['basis'] = data['payslip']['basic_pay'] + data['payslip']['tot_inc_pagibig'] + data['pagibig']['prev_basic_pay'] + data['pagibig']['prev_tot_inc_pagibig']
    return data
