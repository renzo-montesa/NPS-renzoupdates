def compute_taxable_earnings(data):
	for key, payslip in data['payslips'].items():
		data['payslips'][key]['taxable_earnings'] = 0.00

		if not 'payslip_entries' in payslip:
			data['payslips'][key]['payslip_entries'] = {}
			continue

		for entry_key, payslip_entry in payslip[key]['payslip_entries']:
			if entry_key in data['pay_elements']:
				if 'is_taxable' in data['pay_elements'][entry_key]:
					if data['pay_elements'][entry_key]['is_taxable'] == 'Y':
						data['payslips'][key]['taxable_earnings'] += payslip_entry['amount']
						continue
