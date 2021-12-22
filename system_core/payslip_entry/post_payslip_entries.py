from api.v1.payslip_entry.model import PayslipEntryModel
from api.v1.employee.model import EmployeeModel
from api.v1.payslip.model import PayslipModel
from api.v1.payslip_info.model import PayslipInfoModel


def post_payslip_entries(data):
    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        payslip = data['payslips'][key]

        if not 'payslip_entries' in payslip:
            continue

        for entry_key, payslip_entry in payslip['payslip_entries'].items():
            post_entry(data['client_db'], payslip['id'], payslip_entry['pay_element_id'], payslip_entry['amount'])


def post_entry(client_db, payslip_id, pay_element_id, amount):
    db_payslip_entry, client_session = PayslipEntryModel.get_by_filter(client_db, payslip_id=payslip_id, pay_element_id=pay_element_id)
    if db_payslip_entry:
        db_payslip_entry.amount = amount
        db_payslip_entry.commit_to_db(client_session)
    else:
        db_payslip_entry = PayslipEntryModel(
            payslip_id=payslip_id,
            pay_element_id=pay_element_id,
            amount=amount
        )
        db_payslip_entry.save_to_db(client_db)
    client_session.close()


def insert_update_payslip_entries(data):
    for entry_key, payslip_entry in data['payslip_entries'].items():
        if 'payslip_id' in payslip_entry:
            post_entry(data['client_db'], payslip_entry['payslip_id'], payslip_entry['pay_element_id'], payslip_entry['amount'])
        else:
            
            
        
            if payslip_entry['employee_number'] not in data['employees']:
                continue

            if payslip_entry['pay_element_code'] not in data['pay_elements']:
                continue

            
            employee_id = data['employees'][payslip_entry['employee_number']]['id']
            payslip_key=payslip_entry['employee_number']+str(data['payroll_period_id'])
            if not payslip:
                payslip = PayslipModel(
                    employee_id = employee_id,
                    payroll_period_id = data['payroll_period_id'],
                    net_pay = 0,
                    take_home = 0,
                    is_finalized = False
                )
                payslip.save_to_db(data['client_db'])
                payslip_id = payslip.id
                payslip.close(data['client_db'])
            else:
                payslip_id =data['payslip_info'][payslip_key]['id']
               
            
            post_entry(data['client_db'], payslip_id, data['pay_elements'][payslip_entry['pay_element_code']]['id'], payslip_entry['amount'])
