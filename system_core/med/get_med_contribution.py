from api.v1.med_table.model import MedTableModel
from api.v1.mandatory_code.model import MandatoryCodeModel
from api.v1.pay_element.model import PayElementModel


def get_med_contribution(data):
    pe_empl_med, pes1 = PayElementModel.get_by_filter(data['client_db'], code="empl_med")
    pe_empr_med, pes2 = PayElementModel.get_by_filter(data['client_db'], code="empr_med")

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

            continue

        med_row = MedTableModel.get_med_row_by_basis(data['payslips'][key]['mandatories']['med']['basis'])

        if med_row:
            if med_row['percentage'] != 0.00:
                total_contribution = round((data['payslips'][key]['mandatories']['med']['basis'] * med_row['percentage']), 2)

                data['payslips'][key]['mandatories']['med']['employee_share'] = round((total_contribution / 2), 2)
                data['payslips'][key]['mandatories']['med']['employer_share'] = round((total_contribution - data['payslips'][key]['mandatories']['med']['employee_share']), 2)
            else:
                data['payslips'][key]['mandatories']['med']['employee_share'] = med_row['empl_share']
                data['payslips'][key]['mandatories']['med']['employer_share'] = med_row['empr_share']

            if pe_empl_med:
                data['payslips'][key]['payslip_entries'][pe_empl_med.code] = {
                    'pay_element_id': pe_empl_med.id,
                    'pay_element_code': pe_empl_med.code,
                    'amount': data['payslips'][key]['mandatories']['med']['employee_share']
                }
            
            if pe_empr_med:
                data['payslips'][key]['payslip_entries'][pe_empr_med.code] = {
                    'pay_element_id': pe_empr_med.id,
                    'pay_element_code': pe_empr_med.code,
                    'amount': data['payslips'][key]['mandatories']['med']['employer_share']
                }

    pes1.close()
    pes2.close()
