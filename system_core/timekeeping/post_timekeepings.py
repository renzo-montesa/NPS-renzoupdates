from api.v1.timekeeping.model import TimekeepingModel
from api.v1.mandatory_code.model import MandatoryCodeModel
from api.v1.employee.model import EmployeeModel
from api.v1.payslip.model import PayslipModel
from api.v1.payslip_info.model import PayslipInfoModel
import sys


def insert_update_timekeepings(data):
    for entry_key, timekeeping in data['timekeepings'].items():


        if 'payslip_id' in timekeeping:
            post_entry(data['client_db'], timekeeping['payslip_id'], timekeeping['tk_element_id'], timekeeping['hours'])
        else:
            
           
            if timekeeping['employee_number'] not in data['employees']:
                continue

            if timekeeping['tk_element_code'] not in data['tk_elements']:
                continue

            employee_id = data['employees'][timekeeping['employee_number']]['id']
            
            payslip_key=timekeeping['employee_number']+str(data['payroll_period_id'])
            if payslip_key not in data['payslip_info']:
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
                payslip_id = data['payslip_info'][payslip_key]['id']
               
            
            post_entry(data['client_db'], payslip_id, data['tk_elements'][timekeeping['tk_element_code']]['id'], timekeeping['hours'])


def post_entry(client_db, payslip_id, tk_element_id, hours):
    db_timekeeping, client_session = TimekeepingModel.get_by_filter(client_db, payslip_id=payslip_id, tk_element_id=tk_element_id)
    if db_timekeeping:
        db_timekeeping.hours = hours
        db_timekeeping.commit_to_db(client_session)
    else:
        db_timekeeping = TimekeepingModel(
            payslip_id=payslip_id,
            tk_element_id=tk_element_id,
            hours=hours
        )
        db_timekeeping.save_to_db(client_db)
    client_session.close()
