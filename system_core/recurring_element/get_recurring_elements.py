from api.v1.recurring_element_info.model import RecurringElementInfoModel


def get_active_recurring(data):
    data['recurring_elements'] = RecurringElementInfoModel.get_by_period(data['client_db'], data['payroll_period']['period_start'])
