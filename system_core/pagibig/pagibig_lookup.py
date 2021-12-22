def lookup_in_table(data):
    lookup_value = data['pagibig']['basis']

    """
    Insert code here to look up basis in pagibig table
    """
    pagibig_table = {}

    if data['pagibig']['is_maximum']:
        lookup_value = pagibig_table['empl_max']

    data['pagibig']['total_empl_share'] = round(pagibig_table['empl_percentage'] * lookup_value, 2)
    data['pagibig']['total_empr_share'] = round(pagibig_table['empr_percentage'] * lookup_value, 2)
    return data
