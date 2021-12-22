from api.v1.timekeeping_info.model import TimekeepingInfoModel
from system_core.helper.array_to_dict import (array_to_dict_by_key)


def get_timekeeping_info(data):
    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        data['payslips'][key]['timekeepings'] = array_to_dict_by_key(TimekeepingInfoModel.get_by_filter(data['client_db'], payslip_id=data['payslips'][key]['id']), 'tk_element_code')
