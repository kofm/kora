from io import BytesIO

import openpyxl as xl
from django.core.files.uploadedfile import SimpleUploadedFile


def make_excel_bytes(data: list) -> BytesIO:
    """
    Build a BytesIO containing a small XLSX with `data` as rows.
    """
    wb = xl.Workbook()
    ws = wb.active

    # Write headers (keys of the first dict)
    headers = list(data[0].keys())
    ws.append(headers)

    # Write each row’s values
    for row in data:
        ws.append([row.get(key, "") for key in headers])

    bio = BytesIO()
    wb.save(bio)
    bio.seek(0)
    return bio


def make_excel_file(data: list) -> SimpleUploadedFile:
    excel_bio = make_excel_bytes(data)
    return SimpleUploadedFile(
        name="test.xlsx",
        content=excel_bio.read(),
        content_type=("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
    )
