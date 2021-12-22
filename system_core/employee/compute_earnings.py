def compute_tax_and_nontax_earnings(data):
	for key in data['module_batch']['batch_keys'][data['module_batch']['current_batch']]:
		payslip = data['payslips'][key]
		data['payslips'][key]['taxable_earnings'] = 0.00
		data['payslips'][key]['nontaxable_earnings'] = 0.00

		if not 'payslip_entries' in payslip:
			data['payslips'][key]['payslip_entries'] = {}
			continue

		for entry_key, payslip_entry in payslip['payslip_entries'].items():
			if entry_key in data['pay_elements']:
				if data['pay_elements'][entry_key]['pay_element_type_code'] == 'earning':
					if 'is_taxable' in data['pay_elements'][entry_key]:
						if data['pay_elements'][entry_key]['is_taxable'] == 'TRUE':
							data['payslips'][key]['taxable_earnings'] += round((payslip_entry['amount'] * data['pay_elements'][entry_key]['multiplier']), 2)
							continue
					data['payslips'][key]['nontaxable_earnings'] += round((payslip_entry['amount'] * data['pay_elements'][entry_key]['multiplier']), 2)
			
		data['payslips'][key]['taxable_earnings'] = round(data['payslips'][key]['taxable_earnings'], 2)
		data['payslips'][key]['nontaxable_earnings'] = round(data['payslips'][key]['nontaxable_earnings'], 2)
