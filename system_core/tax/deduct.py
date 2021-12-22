def deduct_monthly(data):
    data['tax']['is_deduct'] = True
    return data

def deduct_semimonthly(data):
    schedule = "2" if (data['employee']['period_number'] % 2) == 0 else "1"
    data['tax']['is_deduct'] = True if schedule in data['company']['tax_schedule_semi'] else False
    return data

def deduct_weekly(data):
    remainder = data['employee']['period_number'] % 4
    schedule = '4' if remainder == 0 else str(remainder)
    data['tax']['is_deduct'] = True if schedule in data['company']['tax_schedule_week'] else False
    return data

def deduct_biweekly(data):
    data['tax']['is_deduct'] = True
    return data
