from api.v1.employee_timekeeping.model import EmployeeTimekeepingModel


fields = {
    'id': 'int',
    'employee_id': 'int',
    'tdefa_reg_hrs': 'float',
    'tdefa_nd1': 'float',
    'tdefa_nd2': 'float',
    'tdefa_ot': 'float',
    'tdefa8_ot': 'float',
    'tdefa_nd1_ot': 'float',
    'tdefa_nd18_ot': 'float',
    'tdefa_nd2_ot': 'float',
    'tdefa_nd28_ot': 'float',
    'defa_reg_hrs': 'float',
    'defa_nd1': 'float',
    'defa_nd2': 'float',
    'defa_ot': 'float',
    'defa8_ot': 'float',
    'defa_nd1_ot': 'float',
    'defa_nd18_ot': 'float',
    'defa_nd2_ot': 'float',
    'defa_nd28_ot': 'float',
    'tardy_exempt': 'str',
    'ut_exempt': 'str',
    'absent_exempt': 'str',
    'nd1_exempt': 'str',
    'nd2_exempt': 'str',
    'ot_exempt': 'str',
    'nd1_ot_exempt': 'str',
    'nd2_ot_exempt': 'str'
}


def insert_update_employee_timekeeping_entries(data):
    for entry_key, record in data['employee_timekeepings'].items():
        post_entry(data['client_db'], record)


def post_entry(client_db, record):
    db_record, client_session = EmployeeTimekeepingModel.get_by_filter(client_db, employee_id=record['employee_id'])
    if db_record:
        update_columns(db_record, record)
        client_session.commit()
    else:
        db_record = EmployeeTimekeepingModel()
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
