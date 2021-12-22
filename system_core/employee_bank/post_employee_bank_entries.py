from api.v1.employee_bank.model import EmployeeBankModel


fields = {
    'id': 'int',
    'employee_id': 'int',
    'bank_id': 'int',
    'account_number': 'str'
}


def insert_update_employee_bank_entries(data):
    for entry_key, record in data['employee_banks'].items():
        post_entry(data['client_db'], record)


def post_entry(client_db, record):
    db_record, client_session = EmployeeBankModel.get_by_filter(client_db, employee_id=record['employee_id'], bank_id=record['bank_id'])
    if db_record:
        update_columns(db_record, record)
        client_session.commit()
    else:
        db_record = EmployeeBankModel()
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
                
        setattr(db_record, field, value)
