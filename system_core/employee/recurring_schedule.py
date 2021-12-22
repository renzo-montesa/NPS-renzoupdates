def current_period_monthly(data):
    data['employee']['recurring_schedule'] = 1

    return data

def current_period_semi(data):
    data['employee']['recurring_schedule'] = "2" if (data['employee']['period_number'] % 2) == 0 else "1"

    return data

def current_period_weekly(data):
    remainder = data['employee']['period_number'] % 4
    data['employee']['recurring_schedule'] = '4' if remainder == 0 else str(remainder)

    return data

def current_period_biweekly(data):
    data['employee']['recurring_schedule'] = 1

    return data
