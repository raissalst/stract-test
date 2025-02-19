def remove_element_from_bidimensional_list_by_index(data, element_index):
    return [row[:element_index] + row[(element_index + 1) :] for row in data]

def replace_element_with_empty_string(data, element_index):
    return [row[:element_index] + [""] + row[element_index + 1:] for row in data]
