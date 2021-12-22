from api.v1.loan_info.model import LoanInfoModel


def get_active_loans(data):
    data['loans'] = LoanInfoModel.get_active_loans(data['client_db'])
