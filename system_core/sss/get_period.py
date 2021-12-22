"""
Get the current period number
"""
def get_period(data):
    """
    Insert code here to get current period number from database.
    """

    data['company']['period_month'] = '1'
    data['company']['period_semi'] = '1'
    data['company']['period_week'] = '1'

    return data
