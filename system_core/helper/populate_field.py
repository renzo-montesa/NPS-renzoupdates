def populate_field(objDictSrc, objArrayDest, lookupKeySrc, lookupKeyDest, fieldSrc, fieldDest=None):
    if fieldDest is None:
        fieldDest = fieldSrc

    for i in range(len(objArrayDest)):
        for key, value in objDictSrc.items():
            if value[lookupKeySrc] == objArrayDest[i][lookupKeyDest]:
                if fieldSrc in value:
                    objArrayDest[i][fieldDest] = value[fieldSrc]

    return objArrayDest


def populate_field_dict(objDictSrc, objDictDest, lookupKeySrc, lookupKeyDest, fieldSrc, fieldDest=None):
    if fieldDest is None:
        fieldDest = fieldSrc
    
    objArrayDest = list(objDictDest.values())
    
    for i in range(len(objArrayDest)):
        for key, value in objDictSrc.items():
            if value[lookupKeySrc] == objArrayDest[i][lookupKeyDest]:
                if fieldSrc in value:
                    objArrayDest[i][fieldDest] = value[fieldSrc]

    return objArrayDest
