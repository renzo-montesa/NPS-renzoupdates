"""
Get the current period number
"""
def get_period(data):
    """
    Insert code here to get current period number from database.
    """

    if not 'company' in data:
        data['company'] = {}

    data['company']['period_monthly'] = '1'
    data['company']['period_semi'] = '1'
    data['company']['period_weekly'] = '1'
    data['company']['period_biweekly'] = '1'
