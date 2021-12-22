from api.v1.payslip_entry_detail.model import PayslipEntryDetailModel


def get_historical_payslip_entries(data):
    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        if not 'historical_payslip_entries' in data['payslips'][key]:
            data['payslips'][key]['historical_payslip_entries'] = []
        
        data['payslips'][key]['historical_payslip_entries'] = PayslipEntryDetailModel.get_historical_payslip_entries_by_employee_id(data['payslips'][key]['employee_id'])
