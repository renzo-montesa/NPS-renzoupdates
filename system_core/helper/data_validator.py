def check_data_type(value, data_type):
  try:
    if data_type == 'str':
      value = str(value)
    if data_type == 'int':
      value = int(value)
    if data_type == 'float':
      value = float(value)
    if data_type == 'bool':
      if value.lower() not in ['1','0','true','false']:
        return False, "invalid boolean value"
      if value.lower() == "true":
        value = 1
      if value.lower() == "false":
        value = 0
      value = bool(int(value))
  except Exception as e:
    return False, str(e)
  return True, ""


def check_if_empty(value, data_type):
  try:
    if data_type == 'str':
      value = str(value)
      if value == "":
        return True
    if data_type == 'int':
      value = int(value)
      if value == 0:
        return True
    if data_type == 'float':
      value = float(value)
      if value == 0.00:
        return True
    if data_type == 'bool':
      if value.lower() not in ['1','0','true','false']:
        return True
  except Exception as e:
    return True
  return False