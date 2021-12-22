from api.v1.loan_payment.model import LoanPaymentModel


check_fields = [
    'deduction_date'
]


fields = {
    'id': 'int',
    'loan_id': 'int',
    'deduction_date': 'str',
    'first_deduction': 'str',
    'amount': 'float',
    'installment_no': 'int',
    'outstanding_balance': 'float',
    'is_posted': 'bool',
    'is_hidden': 'bool'
}


def insert_update_loan_payments(data):
    for entry_key, record in data['loans'].items():
        post_entry(data['client_db'], record)


def post_entry(client_db, record):
    db_record, client_session = LoanPaymentModel.get_by_filter(client_db, loan_id=record['loan_id'], deduction_date=record['deduction_date'])
    if db_record:
        update_columns(db_record, record)
        client_session.commit()
    else:
        db_record = LoanPaymentModel()
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
