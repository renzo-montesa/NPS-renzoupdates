from api.v1.pay_element_info.model import PayElementInfoModel
from api.v1.pay_element_property_info.model import PayElementPropertyInfoModel


def get_pay_elements(data):
    pay_elements = PayElementInfoModel.get_pay_elements(data['client_db'])
    data['pay_elements'] = get_pay_element_properties(data['client_db'], pay_elements)


def get_pay_element_properties(client_db, pay_elements):
    formatted = {}

    for pay_element in pay_elements:
        pay_element_properties = PayElementPropertyInfoModel.get_pay_element_properties(client_db, pay_element['id'])

        formatted_properties = {
            'id': pay_element['id'],
            'pay_element_type_id': pay_element['pay_element_type_id'],
            'pay_element_type_code': pay_element['pay_element_type_code'],
            'pay_element_code': pay_element['pay_element_code'],
            'pay_element_description': pay_element['pay_element_description'],
            'formula': pay_element['formula'],
            'multiplier': pay_element['multiplier']
        }

        for pay_element_property in pay_element_properties:
            formatted_properties[pay_element_property['pay_element_property']] = pay_element_property['pay_element_value']
        
        formatted[pay_element['pay_element_code']] = formatted_properties

    return formatted
