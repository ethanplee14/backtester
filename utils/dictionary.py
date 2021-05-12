
def map_dict_list(dict_list, *fields):
    def map_filter(dic): return {field: dic[field] for field in fields}
    return list(map(map_filter, dict_list))


def slice_dict(dic, *fields):
    return {dic[field] for field in fields}
