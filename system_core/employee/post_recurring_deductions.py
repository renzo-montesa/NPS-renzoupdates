def post_recurring_deductions(data):
    recurring_deductions = {}

    for deduction in recurring_deductions:
        if data['employee']['recurring_schedule'] in deduction['schedule']:
            """
            Insert code here to post deduction to ded_detl
            """
            pass

    return data
