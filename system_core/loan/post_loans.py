from api.v1.loan.model import LoanModel


check_fields = [
    'first_deduction'
]


fields = {
    'id': 'int',
    'employee_id': 'int',
    'schedule_id': 'int',
    'loan_code_id': 'int',
    'loan_date': 'str',
    'first_deduction': 'str',
    'loan_amount': 'float',
    'principal_amount': 'float',
    'outstanding_balance': 'float',
    'installment_amount': 'float',
    'is_suspended': 'bool',
    'is_stopped': 'bool',
    'no_of_installment': 'int',
    'remarks': 'str',
    'last_installment_no': 'int'
}


def insert_update_loan_entries(data):
    for entry_key, record in data['loans'].items():
        post_entry(data['client_db'], record)


def post_entry(client_db, record):
    db_record, client_session = LoanModel.get_by_filter(client_db, employee_id=record['employee_id'], loan_code_id=record['loan_code_id'], loan_date=record['loan_date'])
    if db_record:
        update_columns(db_record, record)
        client_session.commit()
    else:
        db_record = LoanModel()
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
