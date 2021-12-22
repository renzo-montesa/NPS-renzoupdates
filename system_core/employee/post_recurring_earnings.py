def post_recurring_earnings(data):
    recurring_earnings = {}

    for earning in recurring_earnings:
        if data['employee']['recurring_schedule'] in earning['schedule']:
            """
            Insert code here to post earning to earndetl
            """
            pass

    return data
