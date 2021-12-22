def create_batches(object, max_per_batch):
    batches = []
    keys = []

    if isinstance(object, dict):
        keys = list(object.keys())
    elif isinstance(object, list):
        keys = object

    batch = 0
    ctr = 1
    for key in keys:
        if ctr == 1:
            batches.append([])

        batches[batch].append(key)
        ctr += 1

        if ctr > max_per_batch:
            batch += 1
            ctr = 1

    return batches
