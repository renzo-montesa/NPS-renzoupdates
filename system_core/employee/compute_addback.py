from system_core.employee.compute_timekeeping import ( compute_timekeeping_standard )


def compute_addback(data):
    compute_timekeeping_standard(data, 'addback', 'rate_day')
