from api.v1.tk_element_info.model import TkElementInfoModel
from system_core.employee.compute_timekeeping import ( compute_timekeeping_standard )


def compute_overtime(data):
    tk_elements = get_overtime_tk_elements(data['client_db'])
    for tk_element in tk_elements:
        compute_timekeeping_standard(data, tk_element['tk_element_code'], 'rate_hour')


def get_overtime_tk_elements(client_db):
    return TkElementInfoModel.get_by_filter(client_db, tk_element_type_code='overtime')
