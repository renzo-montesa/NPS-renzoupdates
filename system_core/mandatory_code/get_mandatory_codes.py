from api.v1.mandatory_code_info.model import MandatoryCodeInfoModel
from system_core.helper.array_to_dict import (array_to_dict_by_key)


def get_mandatory_codes(data):
    data['mandatory_codes'] = array_to_dict_by_key(MandatoryCodeInfoModel.get_mandatory_codes(), 'mandatory_code')