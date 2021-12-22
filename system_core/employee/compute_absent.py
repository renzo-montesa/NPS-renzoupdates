from system_core.employee.compute_timekeeping import ( compute_timekeeping_standard )


def compute_absent(data):
    compute_timekeeping_standard(data, 'absent', 'rate_day')
