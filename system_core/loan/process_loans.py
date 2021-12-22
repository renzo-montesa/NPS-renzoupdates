from system_core.employee.get_period_number import get_period_number


def process_active_loans(data):
    if not 'employees' in data:
        return

    if not 'payroll_period' in data:
        return

    for loan in data['loans']:
        employee_id = loan['employee_id']
        if not employee_id in data['employees']:
            continue

        period_number = get_period_number(data['company'], data['employees'][employee_id]['pay_code'])

        if not period_number in data['payroll_period']['schedule_code']:
            continue

        if not period_number in loan['schedule_code']:
            continue

        if loan['outstanding_balance'] == 0.00:
            continue

        if loan['first_deduction'] > data['payroll_period']['period_start']:
            continue

        if loan['is_suspended']:
            continue

        if employee_id not in data['payslips']:
            continue

        if not 'payslip_entries' in data['payslips'][employee_id]:
            data['payslips'][employee_id]['payslip_entries'] = {}

        amount = loan['installment_amount'] if loan['installment_amount'] < loan['outstanding_balance'] else loan['outstanding_balance']

        data['payslips'][employee_id]['payslip_entries'][loan['pay_element_code']] = {
            'pay_element_id': loan['pay_element_id'],
            'pay_element_code': loan['pay_element_code'],
            'amount': amount
        }
