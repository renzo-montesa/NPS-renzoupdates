def compute_per_group_by_key(data, group_key, sum_key):
    sum_data = {}
    
    if isinstance(data, dict):
        for key, value in data.items():
            if group_key not in value:
                continue

            if sum_key not in value:
                continue

            if value[group_key] is None:
                group_index = ""
            else:
                group_index = value[group_key]

            if group_index not in sum_data:
                sum_data[group_index] = {}
                for field in value:
                    sum_data[group_index][field] = value[field]
            else:
                sum_data[group_index][sum_key] += value[sum_key]

    elif isinstance(data, list):
        for value in data:
            if group_key not in value:
                continue

            if sum_key not in value:
                continue

            if value[group_key] is None:
                group_index = ""
            else:
                group_index = value[group_key]

            if group_index not in sum_data:
                sum_data[group_index] = {}
                for field in value:
                    sum_data[group_index][field] = value[field]
            else:
                sum_data[group_index][sum_key] += value[sum_key]

    return sum_data