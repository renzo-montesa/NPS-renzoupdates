def get_month_previous_data(data):
    """
    Insert code here to get the current month previous data
    """

    data['employee']['pagibig']['prev_empl_pagibig'] = 0.00
    data['employee']['pagibig']['prev_empr_pagibig'] = 0.00
    data['employee']['pagibig']['prev_basic_pay'] = 0.00
    data['employee']['pagibig']['prev_absences'] = 0.00
    data['employee']['pagibig']['prev_tardiness'] = 0.00
    data['employee']['pagibig']['prev_undertime'] = 0.00
    data['employee']['pagibig']['prev_tot_incpagibig'] = 0.00

    return data
