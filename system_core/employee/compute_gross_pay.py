def compute_gross_pay(data):
	for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
		payslip = data['payslips'][key]
		data['payslips'][key]['gross_pay'] = 0.00

		if 'taxable_earnings' in payslip:
			data['payslips'][key]['gross_pay'] = data['payslips'][key]['taxable_earnings']
