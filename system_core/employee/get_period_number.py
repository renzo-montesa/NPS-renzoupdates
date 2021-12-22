def get_period_number(company, paycode):
    if paycode == 'M':
        return company['period_monthly']
    if paycode == 'S':
        return company['period_semi']
    if paycode == 'W':
        return company['period_weekly']
    if paycode == 'B':
        return company['period_biweekly']
    
    return 0
