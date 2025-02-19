from flask import jsonify
from http import HTTPStatus
from app.utils.csv_utils import generate_csv
from app.services.platform_service import get_a_platform_data
from app.exceptions.services_exceptions import ServiceError
from app.external_api.stract_api_service import fetch_platforms
from app.services.common_service import remove_data_from_column, collapse_data
from app.utils.list_utils import remove_element_from_bidimensional_list_by_index

def get_a_platform(platform):
    try:
        platform_list = fetch_platforms()

        if len(platform_list)==0:
            raise ServiceError("Platform not found", HTTPStatus.NOT_FOUND)
        platform_object = next((p for p in platform_list if p["value"] == platform), None)
        if not platform_object:
            raise ServiceError("Platform not found", HTTPStatus.NOT_FOUND)
        
        column_title_list, data_list = get_a_platform_data(platform_object)

        # print(data_list)
        # print(column_title_list)
  
        data_without_token_list, column_title_without_token_list = remove_data_from_column(data_list, column_title_list, 2)

        # print("***************************", column_title_without_token_list)
        
        # print("***************************", data_without_token_list)

        # reordered_data_values_without_token_list = remove_element_from_bidimensional_list_by_index(reordered_data_values_list, 2)
        # column_title_list.pop(2)

        sort_by_list = ["Account"]
        return generate_csv(column_title_without_token_list, data_without_token_list, sort_by_list)
    except ServiceError as e:
        return jsonify(e.to_dict()), e.status_code

def get_a_platform_user_collapsed(platform):
    try:
        platform_list = fetch_platforms()

        if not platform_list:
            raise ServiceError("Platforms not found", HTTPStatus.NOT_FOUND)
        
        platform_object = next((p for p in platform_list if p["value"] == platform), None)
        if not platform_object:
            raise ServiceError("Platform not found", HTTPStatus.NOT_FOUND)
        
        column_title_list, data_list = get_a_platform_data(platform_object)
        # print("platform", column_title_list)

        index_of_token = column_title_list.index("Token")
 
        collapsed_data_list = collapse_data(data_list, index_of_token)
        
        collapsed_data_without_token_list, column_title_without_token_list = remove_data_from_column(collapsed_data_list, column_title_list, index_of_token)
        sort_by_list = ["Account"]

        return generate_csv(column_title_without_token_list, collapsed_data_without_token_list, sort_by_list)

    except ServiceError as e:
        return jsonify(e.to_dict()), e.status_code





# from os import getenv
# import json
# import http.client
# from urllib.parse import urlparse
# from http import HTTPStatus
# import csv
# import io
# from flask import Response

# def get_a_platform(platform):
#     url = getenv("STRACT_URL")
#     secret = getenv("STRACT_API_TOKEN")
#     platform_list = []
#     account_list = []
#     account_page = 1
#     field_list = []
#     field_page = 1
#     insight_list = []

#     parsed_url = urlparse(url)
#     host = parsed_url.netloc  # Extracts "sidebar.stract.to"
#     path = parsed_url.path if parsed_url.path else "/"  # Ensures a valid path

#     conn = http.client.HTTPSConnection(host)
#     headers = {
#         "Authorization": f"Bearer {secret}",
#         "Content-Type": "application/json"
#     }

#     conn.request("GET", path + "/api/platforms", headers=headers)
#     platforms_response = conn.getresponse()

#     if platforms_response.status != 200:
#         return {"error": "Failed to fetch platform data", "status_code": platforms_response.status}
    
#     plataform_response_data = json.loads(platforms_response.read().decode("utf-8"))

#     platform_list.extend(plataform_response_data.get("platforms", []))
#     platform_object = next((p for p in platform_list if p["value"] == platform), None)

#     if platform_object == None:
#         return {"error": "Platform not found", "status_code": HTTPStatus.NOT_FOUND}, HTTPStatus.NOT_FOUND

#     platform_object_value = platform_object["value"]
#     while True:
#         conn.request("GET", f"{path}/api/accounts?platform={platform_object_value}&page={account_page}", headers=headers)
#         accounts_response = conn.getresponse()

#         if accounts_response.status != 200:
#             return {"error": "Failed to fetch accounts data", "status_code": accounts_response.status}
        
#         accounts_response_data = json.loads(accounts_response.read().decode("utf-8"))

#         account_list.extend(accounts_response_data.get("accounts", []))

#         current_page = accounts_response_data["pagination"]["current"]
#         total_pages = accounts_response_data["pagination"]["total"]

#         if current_page >= total_pages:
#             break

#         account_page += 1


#     while True:
#         conn.request("GET", f"{path}/api/fields?platform={platform_object_value}&page={field_page}", headers=headers)
#         fields_response = conn.getresponse()

#         if fields_response.status != 200:
#             return {"error": "Failed to fetch fielfd data", "status_code": fields_response.status}
        
#         fields_response_data = json.loads(fields_response.read().decode("utf-8"))

#         field_list.extend(fields_response_data.get("fields", []))
#         current_page = fields_response_data["pagination"]["current"]
#         total_pages = fields_response_data["pagination"]["total"]

#         if current_page >= total_pages:
#             break

#         field_page += 1


#     reorder_title_list = ["Platform", "Name", "Token"]
#     field_value_list = [f["value"] for f in field_list]
#     field_value_param = ",".join(field_value_list)
#     reorder_title_list[1:1] = field_value_list

#     for account in account_list:
#         conn.request("GET", f"{path}/api/insights?platform={platform_object_value}&account={account['id']}&token={account['token']}&fields={field_value_param}", headers=headers)
#         insights_response = conn.getresponse()
#         if insights_response.status != 200:
#             return {"error": "Failed to fetch insights data", "status_code": insights_response.status}
        
#         insight_response_data = json.loads(insights_response.read().decode("utf-8"))
#         insight_response_list = insight_response_data.get("insights", [])

#         if len(insight_response_list) == 0:
#             return {"error": "Insights not found", "status_code": HTTPStatus.NOT_FOUND}, HTTPStatus.NOT_FOUND

#         append_platform_and_user_info_to_insight_list(insight_response_list, platform, account["name"], account["token"])
#         insight_list.extend(insight_response_data.get("insights", []))

#     reordered_data = reorder_keys(insight_list, reorder_title_list)
#     reordered_data_values_list = convert_to_bidimensional_list(reordered_data)

#     field_text_list = [f["text"] for f in field_list]
#     column_title_list = ["Platform", "Name", "Token"]
#     column_title_list[1:1] = field_text_list
#     conn.close()

#     output = io.StringIO()
#     writer = csv.writer(output)
#     writer.writerow(column_title_list)
#     writer.writerows(reordered_data_values_list)
#     response = Response(output.getvalue(), content_type="text/csv")
#     response.headers["Content-Disposition"] = "attachment; filename=data.csv"
#     return response

#     # return {"message": "oiii"}

# def reorder_keys(data, keys_order):
#     return [{key: d[key] for key in keys_order if key in d} for d in data]

# def append_platform_and_user_info_to_insight_list(insight_list, platform_name, user_name, user_token):
#     for insight in insight_list:
#         insight["Platform"] = platform_name
#         insight["Name"] = user_name
#         insight["Token"] = user_token
#     return insight_list

# def convert_to_bidimensional_list(data):
#     return [list(obj.values()) for obj in data]
