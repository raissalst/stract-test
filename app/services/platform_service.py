from app.external_api.stract_api_service import fetch_accounts, fetch_insights, fetch_fields
from app.utils.dict_utils import reorder_keys, convert_to_bidimensional_list, replace_keys_with_correspondence
from app.exceptions.services_exceptions import ServiceError

def get_a_platform_data(platform_object):
    try:
        platform_value = platform_object.get("value", "")
        platform_name = platform_object.get("text", "")
        account_list = fetch_accounts(platform_value)
        field_list = fetch_fields(platform_value)

        main_column_list = ["Platform", "Account", "Token"]
        field_value_list = [f["value"] for f in field_list]
        field_text_list = sorted([f["text"] for f in field_list])
        field_value_param = ",".join(field_value_list)
        # reorder_title_list[1:1] = field_value_list

        insight_list = fetch_insights(platform_value, platform_name, account_list, field_value_param)
        # print(insight_list)
        # print(insight_list)
        platform_data_with_text_keys = replace_keys_with_correspondence(insight_list, field_list)
        # print(platform_data_with_text_keys)
        reordered_data = reorder_keys(platform_data_with_text_keys, (main_column_list+field_text_list))
        # print(main_column_list+field_value_list)
        # print(reordered_data)
        reordered_data_values_list = convert_to_bidimensional_list(reordered_data)
        # print(reordered_data_values_list)

        return (main_column_list+field_text_list), reordered_data_values_list
    
    except ServiceError as e:
        raise


# def collapse_data_by_user_token(data):
#     collapsed_data = {}

#     for row in data:
#         token = row[2]  # ✅ Token is now the 3rd column (index 2)

#         if token not in collapsed_data:
#             collapsed_data[token] = row[:]  # Copy row as a new entry
#         else:
#             for i in range(3, len(row)):  # ✅ Skip first 3 columns (keep them)
#                 if isinstance(row[i], (int, float)):  # ✅ Sum numeric values
#                     collapsed_data[token][i] += row[i]
#                 else:
#                     collapsed_data[token][i] = ""  # ✅ Remove text for repeated tokens

#     # ✅ Format output: truncate numbers to 3 decimal places & clear non-numeric values for unique tokens
#     final_result = []
#     for token, row in collapsed_data.items():
#         count = sum(1 for r in data if r[2] == token)  # ✅ Count occurrences of this token

#         formatted_row = [
#             round(value, 3) if isinstance(value, float) else value  # ✅ Truncate decimals
#             for value in row
#         ]

#         # ✅ If token appears only once, clear non-numeric values except first 3 columns
#         if count == 1:
#             for i in range(3, len(row)):  # ✅ Skip first 3 columns
#                 if not isinstance(row[i], (int, float)):
#                     formatted_row[i] = ""

#         final_result.append(formatted_row)

#     # print(final_result)

#     return final_result  # ✅ Return the cleaned, collapsed 2D list


