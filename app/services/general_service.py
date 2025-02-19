from app.services.platform_service import get_a_platform_data


def calculate_cost_per_click(column_value_list, data_list):
    index_of_column_from_cost_per_click = column_value_list.index("Cost Per Click")
    index_of_column_from_clicks = column_value_list.index("Clicks")
    index_of_column_from_spend = column_value_list.index("Spend")

    for data_list_item in data_list:
        if data_list_item[index_of_column_from_cost_per_click] == "":
            data_list_item[index_of_column_from_cost_per_click] = round(
                data_list_item[index_of_column_from_spend]
                / data_list_item[index_of_column_from_clicks],
                3,
            )
    return data_list


def get_all_platforms_data(platform_list):
    all_column_titles = set()
    all_platform_data = []
    platform_data_dicts = []

    for platform_object in platform_list:
        column_title_list, reordered_data_values_list = get_a_platform_data(
            platform_object
        )

        all_column_titles.update(column_title_list)

        for row in reordered_data_values_list:
            row_dict = dict(zip(column_title_list, row))
            platform_data_dicts.append(row_dict)

    first_three_columns = ["Platform", "Account", "Token"]
    remaining_columns = sorted(
        col for col in all_column_titles if col not in first_three_columns
    )
    final_column_titles = first_three_columns + remaining_columns

    all_platform_data = [
        [row_dict.get(col, "") for col in final_column_titles]
        for row_dict in platform_data_dicts
    ]

    all_platform_final_data = calculate_cost_per_click(
        final_column_titles, all_platform_data
    )

    return final_column_titles, all_platform_final_data
