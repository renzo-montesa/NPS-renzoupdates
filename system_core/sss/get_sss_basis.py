def get_sss_basis(data):
    get_sss_basis_b_method_n(data)

def get_sss_basis_g_method_r(data):
    data['sss']['basis'] = 0.00
    return data

def get_sss_basis_gb_method_q(data):
    data['sss']['basis'] = data['employee']['rate_month']
    return data

def get_sss_basis_g_method_not_q(data):
    data['sss']['basis'] = data['payslip']['gross_pay'] + data['payslip']['sss_include'] + data['sss']['prev_gross_pay'] + data['sss']['prev_tot_incsss']
    return data

def get_sss_basis_b_method_a(data):
    data['sss']['basis'] = data['payslip']['basic_pay'] + data['payslip']['sss_include'] + data['sss']['prev_basic_pay'] + data['sss']['prev_tot_incsss'] + data['sss']['prev_nd1'] + data['sss']['prev_nd2']
    return data

def get_sss_basis_b_method_n(data):
    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        payslip = data['payslips'][key]
        if not 'mandatories' in payslip:
            data['payslips'][key]['mandatories'] = {}
        
        if not 'sss' in data['payslips'][key]['mandatories']:
            data['payslips'][key]['mandatories']['sss'] = {
                'mandatory_code': 'sss',
                'basis': 0.00,
                'include_basis': 0.00,
                'employee_share': 0.00,
                'employer_share': 0.00,
                'ecc': 0.00
            }
        
        if not 'payslip_entries' in payslip:
            data['payslips'][key]['payslip_entries'] = {}
            continue

        if 'basic_pay' in payslip['payslip_entries']:
            data['payslips'][key]['mandatories']['sss']['basis'] = data['payslips'][key]['mandatories']['sss']['include_basis'] + payslip['payslip_entries']['basic_pay']['amount']

    """data['sss']['basis'] = data['payslip']['basic_pay'] + data['payslip']['sss_include'] + data['sss']['prev_basic_pay'] + data['sss']['prev_tot_incsss']"""

def get_sss_basis_b_method_r(data):
    basis_amount = data['employee']['rate_month'] if data['sss']['is_last_sched'] else data['payslip']['basic_pay']
    data['sss']['basis'] = basis_amount + data['payslip']['sss_include']
    return data

def get_sss_basis_m(data):
    """
    Insert code here to get the maximum range in sss table
    """
    data['sss']['basis'] = 9999999999.99
    return data

def get_sss_basis_t(data):
    """
    Insert code here to get the total amount of recurring earnings of an employee
    """
    data['sss']['basis'] = data['payslip']['gross_pay'] + data['payslip']['nontax_ear'] + (data['employee']['rate_month'] / 2) + data['payslip']['tot_recearn'] + data['sss']['prev_gross_pay'] + data['sss']['prev_tot_incsss']
    return data
