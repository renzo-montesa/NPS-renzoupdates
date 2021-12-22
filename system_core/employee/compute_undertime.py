from system_core.employee.convert_time_format import convert_to_hhmm
from system_core.employee.compute_timekeeping import ( compute_timekeeping_standard )


def compute_undertime(data):
    compute_timekeeping_standard(data, 'undertime', 'rate_hour')

    """data['employee']['payslip']['undertime'] = 0.00
    hours = data['employee']['timesheet']['undertime']

    if data['company']['undertime_format'] == "B":
        hours = convert_to_hhmm(hours)
    
    if data['employee']['undertime_exempt'] != "Y" and data['employee']['month_dail'] == "M":
        data['employee']['payslip']['undertime'] = round(hours * data['employee']['undertime_rate'], data['company']['undertime_decimal'])

    return data"""
