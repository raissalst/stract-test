from app.utils.list_utils import remove_element_from_bidimensional_list_by_index


def remove_data_from_column(data_list, column_list, index):
    data_without_token_list = remove_element_from_bidimensional_list_by_index(
        data_list, index
    )
    column_list.pop(index)
    return data_without_token_list, column_list


def collapse_data(data, collapse_index):
    collapsed_data = {}

    for row in data:
        key = row[collapse_index]

        if key not in collapsed_data:
            collapsed_data[key] = row[:]
        else:
            for i in range(3, len(row)):
                if i != collapse_index:
                    if isinstance(row[i], (int, float)):
                        collapsed_data[key][i] += row[i]
                    else:
                        collapsed_data[key][i] = ""

    final_result = []
    for key, row in collapsed_data.items():
        count = sum(1 for r in data if r[collapse_index] == key)

        formatted_row = [
            (round(value, 3) if isinstance(value, float) else value) for value in row
        ]

        if count == 1:
            for i in range(3, len(row)):
                if i != collapse_index and not isinstance(
                    formatted_row[i], (int, float)
                ):
                    formatted_row[i] = ""

        final_result.append(formatted_row)

    return final_result
