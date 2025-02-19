from http import HTTPStatus

from flask import jsonify

from app.exceptions.services_exceptions import ServiceError
from app.external_api.stract_api_service import fetch_platforms
from app.services.common_service import collapse_data, remove_data_from_column
from app.services.platform_service import get_a_platform_data
from app.utils.csv_utils import generate_csv
from app.utils.list_utils import remove_element_from_bidimensional_list_by_index


def get_a_platform(platform):
    try:
        platform_list = fetch_platforms()

        if len(platform_list) == 0:
            raise ServiceError("Platform not found", HTTPStatus.NOT_FOUND)
        platform_object = next(
            (p for p in platform_list if p["value"] == platform), None
        )
        if not platform_object:
            raise ServiceError("Platform not found", HTTPStatus.NOT_FOUND)

        column_title_list, data_list = get_a_platform_data(platform_object)

        data_without_token_list, column_title_without_token_list = (
            remove_data_from_column(data_list, column_title_list, 2)
        )

        sort_by_list = ["Account"]
        return generate_csv(
            column_title_without_token_list, data_without_token_list, sort_by_list
        )
    except ServiceError as e:
        return jsonify(e.to_dict()), e.status_code


def get_a_platform_user_collapsed(platform):
    try:
        platform_list = fetch_platforms()

        if not platform_list:
            raise ServiceError("Platforms not found", HTTPStatus.NOT_FOUND)

        platform_object = next(
            (p for p in platform_list if p["value"] == platform), None
        )
        if not platform_object:
            raise ServiceError("Platform not found", HTTPStatus.NOT_FOUND)

        column_title_list, data_list = get_a_platform_data(platform_object)

        index_of_token = column_title_list.index("Token")

        collapsed_data_list = collapse_data(data_list, index_of_token)

        collapsed_data_without_token_list, column_title_without_token_list = (
            remove_data_from_column(
                collapsed_data_list, column_title_list, index_of_token
            )
        )
        sort_by_list = ["Account"]

        return generate_csv(
            column_title_without_token_list,
            collapsed_data_without_token_list,
            sort_by_list,
        )

    except ServiceError as e:
        return jsonify(e.to_dict()), e.status_code
