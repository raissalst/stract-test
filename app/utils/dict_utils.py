def reorder_keys(data, keys_order):
    return [{key: d[key] for key in keys_order if key in d} for d in data]

def append_platform_and_user_info_to_insight_list(insight_list, platform_name, user_name, user_token):
    for insight in insight_list:
        insight["Platform"] = platform_name
        insight["Account"] = user_name
        insight["Token"] = user_token
    return insight_list

def convert_to_bidimensional_list(data):
    return [list(obj.values()) for obj in data]

def replace_keys_with_correspondence(data_list, correspondences):
    mapping = {entry["value"]: entry["text"] for entry in correspondences}
    transformed_data = [
        {mapping.get(key, key): value for key, value in entry.items()} for entry in data_list
    ]
    return transformed_data
