def compute_other_earnings(data):
    data['employee']['payslip']['taxable_ea'] = 0.00
    data['employee']['payslip']['nontax_ear'] = 0.00

    """
    Insert code here to get earnings in earndetl
    """
    earnings = {}

    for earning in earnings:
        if earning['taxable'] == "Y":
            data['employee']['payslip']['taxable_ea'] += earning['amount']
        else:
            if earning['hidden'] != "Y"
            data['employee']['payslip']['nontax_ear'] += earning['amount']

    """
    Replace all posted in earndetl with POSTED 'Y'
    Check if this is still necessary
    """

    return data
