from system_core.employee.compute_timekeeping import ( compute_timekeeping_standard )


def compute_paid_holiday(data):
    compute_timekeeping_standard(data, 'paid_holiday', 'rate_day')
