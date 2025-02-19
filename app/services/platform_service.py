from app.exceptions.services_exceptions import ServiceError
from app.external_api.stract_api_service import (
    fetch_accounts,
    fetch_fields,
    fetch_insights,
)
from app.utils.dict_utils import (
    convert_to_bidimensional_list,
    reorder_keys,
    replace_keys_with_correspondence,
)


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

        insight_list = fetch_insights(
            platform_value, platform_name, account_list, field_value_param
        )

        platform_data_with_text_keys = replace_keys_with_correspondence(
            insight_list, field_list
        )
        reordered_data = reorder_keys(
            platform_data_with_text_keys, (main_column_list + field_text_list)
        )

        reordered_data_values_list = convert_to_bidimensional_list(reordered_data)

        return (main_column_list + field_text_list), reordered_data_values_list

    except ServiceError as e:
        raise
