from api.v1.sss_table.model import SssTableModel
from api.v1.sss_prov_table.model import SssProvTableModel
from api.v1.pay_element.model import PayElementModel


def get_sss_contribution(data):
    pe_empl_sss, pes1 = PayElementModel.get_by_filter(data['client_db'], code="empl_sss")
    pe_empr_sss, pes2 = PayElementModel.get_by_filter(data['client_db'], code="empr_sss")
    pe_ecc, pes3 = PayElementModel.get_by_filter(data['client_db'], code="ecc")

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

            continue

        sss_row = SssTableModel.get_sss_row_by_basis(data['payslips'][key]['mandatories']['sss']['basis'])

        if sss_row:
            if sss_row['empl_share'] is not None:
                data['payslips'][key]['mandatories']['sss']['employee_share'] = sss_row['empl_share']
                data['payslips'][key]['mandatories']['sss']['employer_share'] = sss_row['empr_share']
                data['payslips'][key]['mandatories']['sss']['ecc'] = sss_row['ecc']

            if pe_empl_sss:
                data['payslips'][key]['payslip_entries'][pe_empl_sss.code] = {
                    'pay_element_id': pe_empl_sss.id,
                    'pay_element_code': pe_empl_sss.code,
                    'amount': data['payslips'][key]['mandatories']['sss']['employee_share']
                }
            
            if pe_empr_sss:
                data['payslips'][key]['payslip_entries'][pe_empr_sss.code] = {
                    'pay_element_id': pe_empr_sss.id,
                    'pay_element_code': pe_empr_sss.code,
                    'amount': data['payslips'][key]['mandatories']['sss']['employer_share']
                }

            if pe_ecc:
                data['payslips'][key]['payslip_entries'][pe_ecc.code] = {
                    'pay_element_id': pe_ecc.id,
                    'pay_element_code': pe_ecc.code,
                    'amount': data['payslips'][key]['mandatories']['sss']['ecc']
                }

    pes1.close()
    pes2.close()
    pes3.close()


def get_sss_prov_contribution(data):
    pe_prov_ee, pes1 = PayElementModel.get_by_filter(data['client_db'], code="prov_ee")
    pe_prov_er, pes2 = PayElementModel.get_by_filter(data['client_db'], code="prov_er")

    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        if not 'prov_ee' in data['payslips'][key]['payslip_entries'] and pe_prov_ee:
            data['payslips'][key]['payslip_entries']["prov_ee"] = {
                'pay_element_id': pe_prov_ee.id,
                'pay_element_code': pe_prov_ee.code,
                'amount': 0.00
            }

        if not 'prov_er' in data['payslips'][key]['payslip_entries'] and pe_prov_er:
            data['payslips'][key]['payslip_entries']["prov_er"] = {
                'pay_element_id': pe_prov_er.id,
                'pay_element_code': pe_prov_er.code,
                'amount': 0.00
            }

        if not pe_prov_ee or not pe_prov_er:
            continue

        if not 'sss' in data['payslips'][key]['mandatories']:
            continue

        sss_row = SssProvTableModel.get_sss_row_by_basis(data['payslips'][key]['mandatories']['sss']['basis'])

        if sss_row:
            if sss_row['employee_share'] is not None:
                data['payslips'][key]['payslip_entries']["prov_ee"] = {
                    'pay_element_id': pe_prov_ee.id,
                    'pay_element_code': pe_prov_ee.code,
                    'amount': sss_row['employee_share']
                }

                data['payslips'][key]['payslip_entries']["prov_er"] = {
                    'pay_element_id': pe_prov_er.id,
                    'pay_element_code': pe_prov_er.code,
                    'amount': sss_row['employer_share']
                }

    pes1.close()
    pes2.close()
