from system_core.employee.convert_time_format import convert_to_hhmm
from system_core.employee.compute_timekeeping import ( compute_timekeeping_standard )


def compute_tardy(data):
    compute_timekeeping_standard(data, 'tardy', 'rate_hour')

    """data['employee']['payslip']['tardiness'] = 0.00
    hours = data['employee']['timesheet']['tardy']

    if data['company']['tardy_format'] == "B":
        hours = convert_to_hhmm(hours)
    
    if data['employee']['tardy_exempt'] != "Y" and data['employee']['month_dail'] == "M":
        data['employee']['payslip']['tardiness'] = round(hours * data['employee']['tardy_rate'], data['company']['tardy_decimal'])

    return data"""
