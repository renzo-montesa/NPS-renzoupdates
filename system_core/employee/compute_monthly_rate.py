def get_rate_month_daily(data):
    return data

def get_rate_month_monthly_paycode_m(data):
    data['employee']['payslip']['rate_month'] = data['employee']['rate_month']

    return data

def get_rate_month_monthly_paycode_b(data):
    data['employee']['payslip']['rate_month'] = (data['employee']['rate_month'] * data['company']['months_in_year']) / data['company']['days_in_year']

    return data

def get_rate_month_monthly_paycode_semi(data):
    data['employee']['payslip']['rate_month'] /= 2

    return data
