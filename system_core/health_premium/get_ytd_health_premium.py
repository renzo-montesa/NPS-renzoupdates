from api.v1.health_premium.model import HealthPremiumModel


def get_ytd_health_premium(data):
    pay_element_code = 'health_premium'

    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        payslip = data['payslips'][key]

        if not 'ytd' in data['payslips'][key]:
            data['payslips'][key]['ytd'] = {}
        
        if not pay_element_code in data['payslips'][key]['ytd']:
            data['payslips'][key]['ytd'][pay_element_code] = 0.00

        if not 'payroll_period' in data:
            continue

        year = int(data['payroll_period']['period_start'][:4])

        health_premium = HealthPremiumModel.get_total_by_employee_and_year(data['payslips'][key]['employee_id'], year)

        if health_premium is not None:
            if health_premium['amount'] is not None:
                data['payslips'][key]['ytd'][pay_element_code] = health_premium['amount']

        if not 'historical_payslip_entries' in data['payslips'][key]:
            continue

        for payslip_entry in payslip['historical_payslip_entries']:
            if payslip_entry['pay_element_code'] not in data['pay_elements']:
                continue

            if 'is_ded_tax' not in data['pay_elements'][payslip_entry['pay_element_code']]:
                continue

            if 'is_health_prem' not in data['pay_elements'][payslip_entry['pay_element_code']]:
                continue

            if data['pay_elements'][payslip_entry['pay_element_code']]['is_ded_tax'] == 'TRUE' and data['pay_elements'][payslip_entry['pay_element_code']]['is_health_prem'] == 'TRUE':
                data['payslips'][key]['ytd'][pay_element_code] += payslip_entry['amount']