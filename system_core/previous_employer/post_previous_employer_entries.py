from api.v1.previous_employer.model import PreviousEmployerModel


fields = {
    'id': 'int',
    'employee_id': 'int',
    'company_name': 'str',
    'address': 'str',
    'telephone': 'str',
    'tin': 'str',
    'rate': 'float',
    'pytd_taxable_earning': 'float',
    'pytd_nontax_earning': 'float',
    'pytd_nontax_bonus': 'float',
    'pytd_taxable_bonus': 'float',
    'pytd_wtax': 'float',
    'pytd_union': 'float',
    'pytd_sss': 'float',
    'pytd_med': 'float',
    'pytd_pagib': 'float'
}


def insert_update_previous_employer_entries(data):
    for entry_key, record in data['previous_employers'].items():
        post_entry(data['client_db'], record)


def post_entry(client_db, record):
    db_record, client_session = PreviousEmployerModel.get_by_filter(client_db, employee_id=record['employee_id'])
    if db_record:
        update_columns(db_record, record)
        client_session.commit()
    else:
        db_record = PreviousEmployerModel()
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
