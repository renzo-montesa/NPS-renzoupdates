def get_distinct_keys(data):
    keys_set = set()

    for arr in data:
        for key in arr:
            keys_set.add(key)

    return list(keys_set)