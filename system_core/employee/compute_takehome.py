def compute_takehome(data):
    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        data['payslips'][key]['take_home'] = data['payslips'][key]['net_pay']
