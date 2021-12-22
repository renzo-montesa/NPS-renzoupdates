import sys
import datetime
import re


def convert_date(date_string):
    try:
        mat = re.match('(\d{2})[/](\d{2})[/](\d{4})$', date_string)
        if mat is not None:
            datetime.datetime.strptime(date_string, "%m/%d/%Y")
            date_string = date_string[6:] + '-' + date_string[0:2] + '-' + date_string[3:5]

        mat = re.match('(\d{4})[-](\d{2})[-](\d{2})$', date_string)
        if mat is not None:
            datetime.datetime.strptime(date_string, "%Y-%m-%d")
            return date_string
    except ValueError:
        print('ValueError', file=sys.stderr)
        pass
    print('Invalid date', file=sys.stderr)
    return None