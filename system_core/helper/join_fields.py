def join_fields_with_key(data, ref_data, ref_key, join_fields):
    join_data = None
    
    if isinstance(data, dict):
        join_data = {}

        for key, value in data.items():
            join_data[key] = join_field(value, ref_data, ref_key, join_fields)

    elif isinstance(data, list):
        join_data = []

        for value in data:
            join_data.append(join_field(value, ref_data, ref_key, join_fields))

    return join_data


def join_field(obj, ref_data, ref_key, join_fields):
    if ref_key not in obj:
        for field in join_fields:
            obj[field] = None

    ref_index = obj[ref_key]

    if ref_index in ref_data:
        for field in join_fields:
            if field in ref_data[ref_index]:
                obj[field] = ref_data[ref_index][field]
            else:
                obj[field] = None
    else:
        for field in join_fields:
            obj[field] = None

    return obj