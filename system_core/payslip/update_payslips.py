from api.v1.payslip.model import PayslipModel
from flask_restful import marshal, fields as mfields
from system_core.helper.array_to_dict import (array_to_dict_by_key)


def update_payslips(data):
    for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
        payslip = data['payslips'][key]

        db_payslip, client_session = PayslipModel.getById(data['client_db'], payslip['id'])
        if db_payslip:
            db_payslip.net_pay = payslip['net_pay']
            db_payslip.take_home = payslip['take_home']
            db_payslip.commit_to_db(client_session)
            
        client_session.close()
