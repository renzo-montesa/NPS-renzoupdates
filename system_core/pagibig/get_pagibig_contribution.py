from api.v1.hdmf_table.model import HdmfTableModel
from api.v1.mandatory_code.model import MandatoryCodeModel
from api.v1.pay_element.model import PayElementModel


def get_pagibig_contribution(data):
    get_contribution_normal(data)


def get_contribution_normal(data):
    pe_empl_pagib, pes1 = PayElementModel.get_by_filter(data['client_db'], code="empl_pagib")
    pe_empr_pagib, pes2 = PayElementModel.get_by_filter(data['client_db'], code="empr_pagib")
    pe_pag_add, pes3 = PayElementModel.get_by_filter(data['client_db'], code="pagibig_additional")

    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        payslip = data['payslips'][key]
        if not 'mandatories' in payslip:
            data['payslips'][key]['mandatories'] = {}
        
        if not 'pagibig' in data['payslips'][key]['mandatories']:
            data['payslips'][key]['mandatories']['pagibig'] = {
                'mandatory_code': 'pagibig',
                'basis': 0.00,
                'include_basis': 0.00,
                'employee_share': 0.00,
                'employer_share': 0.00,
                'pagibig_additional': 0.00
            }

            continue

        if key not in data['employees']:
            continue

        hdmf_row = HdmfTableModel.get_hdmf_row_by_basis(data['payslips'][key]['mandatories']['pagibig']['basis'])

        if hdmf_row:
            lookupValue = data['payslips'][key]['mandatories']['pagibig']['basis']

            if lookupValue > hdmf_row['empl_max'] or data['employees'][key]['is_pagibig_max']:
                lookupValue = hdmf_row['empl_max']

            data['payslips'][key]['mandatories']['pagibig']['employee_share'] = round(hdmf_row['empl_percent'] * lookupValue, 2)
            data['payslips'][key]['mandatories']['pagibig']['employer_share'] = round(hdmf_row['empr_percent'] * lookupValue, 2)

            if data['employees'][key]['pagibig_additional']:
                data['payslips'][key]['mandatories']['pagibig']['employee_share'] += data['employees'][key]['pagibig_additional']

            if pe_empl_pagib:
                data['payslips'][key]['payslip_entries'][pe_empl_pagib.code] = {
                    'pay_element_id': pe_empl_pagib.id,
                    'pay_element_code': pe_empl_pagib.code,
                    'amount': data['payslips'][key]['mandatories']['pagibig']['employee_share']
                }
            
            if pe_empr_pagib:
                data['payslips'][key]['payslip_entries'][pe_empr_pagib.code] = {
                    'pay_element_id': pe_empr_pagib.id,
                    'pay_element_code': pe_empr_pagib.code,
                    'amount': data['payslips'][key]['mandatories']['pagibig']['employer_share']
                }

            if pe_pag_add and data['employees'][key]['pagibig_additional'] > 0:
                data['payslips'][key]['payslip_entries'][pe_pag_add.code] = {
                    'pay_element_id': pe_pag_add.id,
                    'pay_element_code': pe_pag_add.code,
                    'amount': data['employees'][key]['pagibig_additional']
                }

    pes1.close()
    pes2.close()
    pes3.close()
