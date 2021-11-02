
def name_dict_from_list(lst):
    return {
        "name": {
            "first_name": lst[0] or "",
            "middle_name": lst[1] or "",
            "last_name": lst[2] or ""
        }
    }


def address_dict_from_str(string):
    addresses = {}
    adds = string.split(";") if string else []

    for add in adds:
        key, value = add.split(":")
        key = key.lower().lstrip()
        values = value.split(",")
        addresses[key] = {
            f"{key}_address": values[0].lstrip() if values[0] else "",
            f"{key}_city": values[1].lstrip() if len(values) > 1 and values[1] else "",
            f"{key}_state": values[2].lstrip() if len(values) > 2 and values[2] else "",
            f"{key}_zip": values[3].lstrip() if len(values) > 3 and values[3] else ""
        }

    return {"addresses": addresses}


def phone_dict_from_str(string):
    phones_ = {}
    phones = string.split(";") if string else []

    for phone in phones:
        ptype, pval = phone.split(":")
        phones_[ptype.lower().lstrip()] = pval.lstrip()

    return {"phones": phones_}


def date_dict_from_str(string):
    dates_ = {}
    dates = string.split(";") if string else []

    for date in dates:
        dtype, dval = date.split(":")
        dates_[dtype.lower().lstrip()] = dval.lstrip()

    return {"dates": dates_}
