def get_med_basis(data):
    get_med_basis_r_monthly(data)

def get_med_basis_g_method_r(data):
    data['med']['basis'] = 0.00
    return data

def get_med_basis_gb_method_q(data):
    data['med']['basis'] = data['employee']['rate_month']
    return data

def get_med_basis_g_method_f(data):
    data['med']['basis'] = data['employee']['rate_month'] + data['payslip']['med_include'] + data['med']['prev_gross_pay'] + data['med']['prev_tot_incmed']
    return data

def get_med_basis_g_method_not_qf(data):
    data['med']['basis'] = data['payslip']['gross_pay'] + data['payslip']['med_include'] + data['med']['prev_gross_pay'] + data['med']['prev_tot_incmed']
    return data

def get_med_basis_b_method_a(data):
    data['med']['basis'] = data['payslip']['basic_pay'] + data['payslip']['med_include'] + data['med']['prev_basic_pay'] + data['med']['prev_tot_incmed'] + data['med']['prev_nd1'] + data['med']['prev_nd2']
    return data

def get_med_basis_b_method_n(data):
    data['med']['basis'] = data['payslip']['basic_pay'] + data['payslip']['med_include'] + data['med']['prev_basic_pay'] + data['med']['prev_tot_incmed']
    return data

def get_med_basis_b_method_r(data):
    basis_amount = data['employee']['rate_month'] if data['med']['is_last_sched'] else data['payslip']['basic_pay']
    data['med']['basis'] = basis_amount + data['payslip']['med_include']
    return data

def get_med_basis_b_method_f(data):
    data['med']['basis'] = data['employee']['rate_month'] + data['payslip']['med_include'] + data['med']['prev_tot_incmed']
    return data

def get_med_basis_m(data):
    """
    Insert code here to get the maximum range in med table
    """
    data['med']['basis'] = 9999999999.99
    return data

def get_med_basis_r_monthly(data):
    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        payslip = data['payslips'][key]
        if not 'mandatories' in payslip:
            data['payslips'][key]['mandatories'] = {}
        
        if not 'med' in data['payslips'][key]['mandatories']:
            data['payslips'][key]['mandatories']['med'] = {
                'mandatory_code': 'med',
                'basis': 0.00,
                'include_basis': 0.00,
                'employee_share': 0.00,
                'employer_share': 0.00
            }

        if key not in data['employees']:
            continue
        
        data['payslips'][key]['mandatories']['med']['basis'] = round(data['employees'][key]['rate_month'], 2)

def get_med_basis_r_daily(data):
    data['med']['basis'] = data['employee']['rate_day'] * data['company']['days_in_year'] / data['company']['months_in_year']
    return data

def get_med_basis_i(data):
    data['med']['basis'] = data['employee']['income_out']
    return data
