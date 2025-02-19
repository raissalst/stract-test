import csv
import io
from flask import Response

def generate_csv(column_title_list, data, sort_by=None):
    if sort_by:
        sort_indices = [column_title_list.index(col) for col in sort_by if col in column_title_list]
        data = sorted(data, key=lambda row: tuple(row[i] for i in sort_indices))

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(column_title_list)
    writer.writerows(data)

    response = Response(output.getvalue(), content_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=response.csv"
    return response