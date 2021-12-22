from api.v1.tax_table_info.model import TaxTableInfoModel
from api.v1.mandatory_code.model import MandatoryCodeModel
from api.v1.pay_element.model import PayElementModel


def compute_tax(data):
    mandatory_code, mcs = MandatoryCodeModel.get_by_filter(data['client_db'], code="tax")

    if mandatory_code:
        pay_element, pes = PayElementModel.get_by_filter(data['client_db'], id=mandatory_code.pay_element_id)

    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        payslip = data['payslips'][key]
        if not 'mandatories' in payslip:
            data['payslips'][key]['mandatories'] = {}
        
        if not 'tax' in data['payslips'][key]['mandatories']:
            data['payslips'][key]['mandatories']['tax'] = {
                'mandatory_code': 'tax',
                'basis': 0.00,
                'employee_share': 0.00
            }

            continue

        tax_table_row = TaxTableInfoModel.get_tax_table_info_row_by_filter('S', 'Z', data['payslips'][key]['mandatories']['tax']['basis'])

        if tax_table_row:
            tax = 0.00
            
            if tax_table_row['lower_limit'] is not None:
                tax = round(((data['payslips'][key]['mandatories']['tax']['basis'] - \
                    tax_table_row['lower_limit']) * tax_table_row['percentage']) + \
                    tax_table_row['fixed_amount'], 2)

            data['payslips'][key]['mandatories']['tax']['employee_share'] = tax

            if mandatory_code and pay_element:
                data['payslips'][key]['payslip_entries'][pay_element.code] = {
                    'pay_element_id': mandatory_code.pay_element_id,
                    'pay_element_code': pay_element.code,
                    'amount': tax
                }

    mcs.close()
    if mandatory_code:
        pes.close()


def compute_tax_f(data):
    mandatory_code, mcs = MandatoryCodeModel.get_by_filter(code="tax")

    if mandatory_code:
        pay_element, pes = PayElementModel.get_by_filter(id=mandatory_code.pay_element_id)

    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        payslip = data['payslips'][key]
        if not 'mandatories' in payslip:
            data['payslips'][key]['mandatories'] = {}
        
        if not 'tax' in data['payslips'][key]['mandatories']:
            data['payslips'][key]['mandatories']['tax'] = {
                'mandatory_code': 'tax',
                'basis': 0.00,
                'employee_share': 0.00
            }

            continue

        tax_table_row = TaxTableInfoModel.get_tax_table_info_row_by_filter('S', 'Z', data['payslips'][key]['mandatories']['tax']['basis'])

        if tax_table_row:
            tax = round(((data['payslips'][key]['mandatories']['tax']['basis'] - \
                tax_table_row['lower_limit']) * tax_table_row['percentage']) + \
                tax_table_row['fixed_amount'], 2)

            data['payslips'][key]['mandatories']['tax']['employee_share'] = tax

            if mandatory_code and pay_element:
                data['payslips'][key]['payslip_entries'][pay_element.code] = {
                    'pay_element_id': mandatory_code.pay_element_id,
                    'pay_element_code': pay_element.code,
                    'amount': tax
                }

    mcs.close()
    if mandatory_code:
        pes.close()
