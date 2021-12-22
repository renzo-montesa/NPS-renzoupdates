from api.v1.recurring_element.model import RecurringElementModel
from system_core.employee.get_period_number import get_period_number
import sys


check_fields = [
    'start_date',
    'end_date'
]


fields = {
    'id': 'int',
    'employee_id': 'int',
    'pay_element_id': 'int',
    'schedule_id': 'int',
    'amount': 'float',
    'is_active': 'bool',
    'start_date': 'str',
    'end_date': 'str',
    'remarks': 'str'
}


def post_recurring_elements(data):
    if not 'employees' in data:
        return

    if not 'payroll_period' in data:
        return

    for recurring_element in data['recurring_elements']:
        employee_id = recurring_element['employee_id']
        if not employee_id in data['employees']:
            continue

        period_number = get_period_number(data['company'], data['employees'][employee_id]['pay_code'])

        if not period_number in data['payroll_period']['schedule_code']:
            continue

        if not period_number in recurring_element['schedule_code']:
            continue

        if not 'payslip_entries' in data['payslips'][employee_id]:
            data['payslips'][employee_id]['payslip_entries'] = {}
            print("No payslip_entries", file=sys.stderr)

        data['payslips'][employee_id]['payslip_entries'][recurring_element['pay_element_code']] = {
            'pay_element_id': recurring_element['pay_element_id'],
            'pay_element_code': recurring_element['pay_element_code'],
            'amount': recurring_element['amount']
        }


def insert_update_recurring_element_entries(data):
    for entry_key, record in data['recurring_elements'].items():
        post_entry(data['client_db'], record)


def post_entry(client_db, record):
    db_record, client_session = RecurringElementModel.get_by_filter(client_db, employee_id=record['employee_id'], pay_element_id=record['pay_element_id'])
    if db_record:
        update_columns(db_record, record)
        client_session.commit()
    else:
        db_record = RecurringElementModel()
        update_columns(db_record, record)
        db_record.save_to_db(client_db)


def update_columns(db_record, record):
    for field, value in record.items():
        if field in fields and value is not None:
            if fields[field] == 'str':
                value = str(value)
            if fields[field] == 'int':
                value = int(value)
            if fields[field] == 'float':
                value = float(value)
            if fields[field] == 'bool':
                value = bool(int(value))

        if field in check_fields:
            if value == '':
                value = None
                
        setattr(db_record, field, value)
