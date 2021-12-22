def get_company_parameters(data):
    if not 'company' in data:
        data['company'] = {}
    
    data['company']['tardy_format'] = 'A'
    data['company']['pagibig_max'] = 100.00
