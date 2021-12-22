from api.v1.payslip_entry_info.model import PayslipEntryInfoModel
from system_core.helper.merge_dicts import merge_two_dicts


def get_payslip_entries(data):
    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        if not 'payslip_entries' in data['payslips'][key]:
            data['payslips'][key]['payslip_entries'] = {}
        
        data['payslips'][key]['payslip_entries'] = merge_two_dicts(data['payslips'][key]['payslip_entries'], PayslipEntryInfoModel.get_payslip_entries_by_payslip_id(data['client_db'], data['payslips'][key]['id']))
