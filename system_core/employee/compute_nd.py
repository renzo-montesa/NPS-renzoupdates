from system_core.employee.compute_timekeeping import ( compute_timekeeping_standard )


def compute_nd1(data):
    compute_timekeeping_standard(data, 'nd1', 'rate_hour')

def compute_nd2(data):
    compute_timekeeping_standard(data, 'nd2', 'rate_hour')
