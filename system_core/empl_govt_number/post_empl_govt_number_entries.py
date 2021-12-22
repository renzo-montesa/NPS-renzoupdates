from api.v1.empl_govt_number.model import EmplGovtNumberModel


fields = {
    'id': 'int',
    'employee_id': 'int',
    'mandatory_code_id': 'int',
    'account_number': 'str',
    'is_exempt': 'bool',
    'basis': 'str'
}


def insert_update_empl_govt_number_entries(data):
    for entry_key, record in data['empl_govt_numbers'].items():
        post_entry(data['client_db'], record)


def post_entry(client_db, record):
    db_record, client_session = EmplGovtNumberModel.get_by_filter(client_db, employee_id=record['employee_id'], mandatory_code_id=record['mandatory_code_id'])
    if db_record:
        update_columns(db_record, record)
        client_session.commit()
    else:
        db_record = EmplGovtNumberModel()
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
