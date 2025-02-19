import http.client
import json
from http import HTTPStatus
from os import getenv
from urllib.parse import urlparse

from app.exceptions.services_exceptions import ServiceError
from app.utils.dict_utils import append_platform_and_user_info_to_insight_list


def get_http_connection():
    url = getenv("STRACT_URL")
    parsed_url = urlparse(url)
    return http.client.HTTPSConnection(parsed_url.netloc), parsed_url.path


def fetch_platforms():
    conn, path = get_http_connection()
    headers = {
        "Authorization": f"Bearer {getenv('STRACT_API_TOKEN')}",
        "Content-Type": "application/json",
    }

    conn.request("GET", f"{path}/api/platforms", headers=headers)
    response = conn.getresponse()

    if response.status != 200:
        raise ServiceError("Failed to fetch platforms data", response.status)

    return json.loads(response.read().decode("utf-8")).get("platforms", [])


def fetch_accounts(platform_value):
    account_list = []
    account_page = 1
    conn, path = get_http_connection()
    headers = {
        "Authorization": f"Bearer {getenv('STRACT_API_TOKEN')}",
        "Content-Type": "application/json",
    }

    while True:
        conn.request(
            "GET",
            f"{path}/api/accounts?platform={platform_value}&page={account_page}",
            headers=headers,
        )
        response = conn.getresponse()

        if response.status != 200:
            raise ServiceError("Failed to fetch accounts data", response.status)

        response_data = json.loads(response.read().decode("utf-8"))
        account_list.extend(response_data.get("accounts", []))

        pagination = response_data.get("pagination")
        if not pagination:
            break

        current_page = pagination.get("current", 1)
        total_pages = pagination.get("total", 1)

        current_page = response_data["pagination"]["current"]
        total_pages = response_data["pagination"]["total"]

        if current_page >= total_pages:
            break
        account_page += 1

    return account_list


def fetch_fields(platform_value):
    field_list = []
    field_page = 1
    conn, path = get_http_connection()
    headers = {
        "Authorization": f"Bearer {getenv('STRACT_API_TOKEN')}",
        "Content-Type": "application/json",
    }

    while True:
        conn.request(
            "GET",
            f"{path}/api/fields?platform={platform_value}&page={field_page}",
            headers=headers,
        )
        response = conn.getresponse()

        if response.status != 200:
            raise ServiceError("Failed to fetch fields data", response.status)

        response_data = json.loads(response.read().decode("utf-8"))
        field_list.extend(response_data.get("fields", []))

        pagination = response_data.get("pagination")
        if not pagination:
            break

        current_page = pagination.get("current", 1)
        total_pages = pagination.get("total", 1)

        current_page = response_data["pagination"]["current"]
        total_pages = response_data["pagination"]["total"]

        if current_page >= total_pages:
            break

        field_page += 1

    return field_list


def fetch_insights(platform_value, platform_name, accounts, field_param):
    insight_list = []
    conn, path = get_http_connection()
    headers = {
        "Authorization": f"Bearer {getenv('STRACT_API_TOKEN')}",
        "Content-Type": "application/json",
    }

    for account in accounts:
        conn.request(
            "GET",
            f"{path}/api/insights?platform={platform_value}&account={account['id']}&token={account['token']}&fields={field_param}",
            headers=headers,
        )
        response = conn.getresponse()

        if response.status != 200:
            raise ServiceError("Failed to fetch insights data", response.status)

        response_data = json.loads(response.read().decode("utf-8")).get("insights", [])

        if not response_data:
            raise ServiceError("Insights not found", HTTPStatus.NOT_FOUND)

        append_platform_and_user_info_to_insight_list(
            response_data, platform_name, account["name"], account["token"]
        )
        insight_list.extend(response_data)

    return insight_list
