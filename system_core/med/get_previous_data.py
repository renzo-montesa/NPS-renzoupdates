def get_month_previous_data(data):
    """
    Insert code here to get the current month previous data
    """

    data['employee']['med']['prev_empl_med'] = 0.00
    data['employee']['med']['prev_empr_med'] = 0.00
    data['employee']['med']['prev_gross_pay'] = 0.00
    data['employee']['med']['prev_basic_pay'] = 0.00
    data['employee']['med']['prev_nd1'] = 0.00
    data['employee']['med']['prev_nd2'] = 0.00
    data['employee']['med']['prev_tot_incmed'] = 0.00

    return data
