def array_to_dict_by_key(objArray, key):
    objDict = {}
    for i in range(len(objArray)):
        objDict[objArray[i][key]] = objArray[i]

    return objDict

def array_to_dict_by_keys(objArray, keys):
    objDict = {}
    for i in range(len(objArray)):
        key = ""
        for x in keys:
            key += objArray[i][x] if type(objArray[i][x]) is str else str(objArray[i][x])
        objDict[key] = objArray[i]

    return objDict


def array_to_dict_by_key_lower(objArray, key):
    objDict = {}
    for i in range(len(objArray)):
        objDict[str(objArray[i][key]).lower()] = objArray[i]

    return objDict


def array_to_dict_by_keys_lower(objArray, keys):
    objDict = {}
    for i in range(len(objArray)):
        key = ""
        for x in keys:
            key += objArray[i][x] if type(objArray[i][x]) is str else str(objArray[i][x])
        objDict[key.lower()] = objArray[i]

    return objDict
