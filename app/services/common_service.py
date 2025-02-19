from app.utils.list_utils import remove_element_from_bidimensional_list_by_index

def remove_data_from_column(data_list, column_list, index):
    data_without_token_list = remove_element_from_bidimensional_list_by_index(data_list, index)
    column_list.pop(index)
    return data_without_token_list, column_list

def collapse_data(data, collapse_index):
    collapsed_data = {}

    for row in data:
        key = row[collapse_index]  # ✅ Use dynamic index for grouping

        if key not in collapsed_data:
            collapsed_data[key] = row[:]  # ✅ Copy the row as a new entry
        else:
            for i in range(3, len(row)):  # ✅ Iterate over all columns
                if i != collapse_index:  # ✅ Skip the grouping column itself
                    if isinstance(row[i], (int, float)):  # ✅ Sum numeric values
                        collapsed_data[key][i] += row[i]
                    else:
                        collapsed_data[key][i] = ""  # ✅ Clear text for repeated values

    # ✅ Format output: truncate numbers to 3 decimal places & clear text for single occurrences
    final_result = []
    for key, row in collapsed_data.items():
        count = sum(1 for r in data if r[collapse_index] == key)  # ✅ Count occurrences

        formatted_row = [
            round(value, 3) if isinstance(value, float) else value  # ✅ Truncate decimals
            for value in row
        ]

        # ✅ If the key appears only once, clear non-numeric values except the grouping column
        if count == 1:
            for i in range(3, len(row)):  # ✅ Iterate over all columns
                if i != collapse_index and not isinstance(formatted_row[i], (int, float)):
                    formatted_row[i] = ""



        final_result.append(formatted_row)

    return final_result  # ✅ Return the cleaned, collapsed 2D list
