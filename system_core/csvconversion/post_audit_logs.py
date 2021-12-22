from api.v1.csv_audit_log.model import CsvAuditLogModel
from api.v1.masterfile_audit_log.model import MasterfileAuditLogModel


def post_audit_logs(data):
    for audit_log in data['audit_logs']:
        db_audit_log = CsvAuditLogModel(
            employee_number = audit_log['employee_number'],
            payroll_period_id = audit_log['payroll_period_id'],
            tablename = audit_log['tablename'],
            field = audit_log['field'],
            code = audit_log['code'],
            old_value = audit_log['old_value'],
            new_value = audit_log['new_value'],
            transaction_type = audit_log['transaction_type'],
            username = audit_log['username']
        )
        db_audit_log.save_to_db(data['client_db'])


def post_masterfile_audit_logs(data):
    for audit_log in data['audit_logs']:
        db_audit_log = MasterfileAuditLogModel(
            employee_number = audit_log['employee_number'],
            tablename = audit_log['tablename'],
            field = audit_log['field'],
            code = audit_log['code'],
            old_value = audit_log['old_value'],
            new_value = audit_log['new_value'],
            transaction_type = audit_log['transaction_type'],
            username = audit_log['username']
        )
        db_audit_log.save_to_db(data['client_db'])
