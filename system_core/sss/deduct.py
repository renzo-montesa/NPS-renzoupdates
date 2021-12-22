"""
Returns true or false if scheduled for deduction
"""
def deduct_monthly(data):
    data['sss']['is_deduct'] = True
    data['sss']['is_last_sched'] = True
    return data

def deduct_semimonthly(data):
    data['sss']['is_last_sched'] = True if (data['employee']['period_number'] % 2) == 0 else False
    schedule = "2" if (data['employee']['period_number'] % 2) == 0 else "1"
    data['sss']['is_deduct'] = True if schedule in data['company']['sss_schedule_semi'] else False
    return data

def deduct_weekly(data):
    remainder = data['employee']['period_number'] % 4
    data['sss']['is_last_sched'] = True if remainder == 0  else False

    schedule = '4' if remainder == 0 else str(remainder)
    data['sss']['is_deduct'] = True if schedule in data['company']['sss_schedule_week'] else False
    return data

def deduct_biweekly(data):
    data['sss']['is_deduct'] = True
    data['sss']['is_last_sched'] = True
    return data
