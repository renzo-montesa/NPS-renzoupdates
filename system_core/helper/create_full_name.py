def create_full_name(lastname, firstname, middlename=None):
    name = lastname + ", " + firstname
    if middlename:
        name += " " + middlename[0] + "."

    return name