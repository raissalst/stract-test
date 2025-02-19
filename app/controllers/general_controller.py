from http import HTTPStatus
from flask import jsonify
from http import HTTPStatus
from app.external_api.stract_api_service import fetch_platforms
from app.exceptions.services_exceptions import ServiceError
from app.utils.csv_utils import generate_csv
from app.services.common_service import remove_data_from_column, collapse_data
from app.services.general_service import get_all_platforms_data


def get_all_platforms():
    try:
        platform_list = fetch_platforms()

        if not platform_list:
            raise ServiceError("Platforms not found", HTTPStatus.NOT_FOUND)
        
        column_title_list, data_list = get_all_platforms_data(platform_list)

        data_without_token_list, column_title_without_token_list = remove_data_from_column(data_list,column_title_list, 2)

        sort_by_list = ["Platform", "Account"]
        # return generate_csv(column_title_list, data_list, sort_by_list)
        return generate_csv(column_title_without_token_list, data_without_token_list, sort_by_list)
    
    except ServiceError as e:
        return jsonify(e.to_dict()), e.status_code


def get_all_platforms_platform_collapsed():
    try:
        platform_list = fetch_platforms()

        if not platform_list:
            raise ServiceError("Platforms not found", HTTPStatus.NOT_FOUND)
        
        column_title_list, data_list = get_all_platforms_data(platform_list)
        # print(column_title_list)

        index_of_platform = column_title_list.index("Platform")
 
        collapsed_data_list = collapse_data(data_list, index_of_platform)

        collapsed_data_without_token_list, column_title_without_token_list = remove_data_from_column(collapsed_data_list, column_title_list, 2)

        sort_by_list = ["Platform", "Account"]
        # return generate_csv(column_title_list, collapsed_data_list, sort_by_list)
        return generate_csv(column_title_without_token_list, collapsed_data_without_token_list, sort_by_list)


    except ServiceError as e:
        return jsonify(e.to_dict()), e.status_code