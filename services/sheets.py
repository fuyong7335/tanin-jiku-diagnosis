# services/sheets.py
# 役割：診断結果を Google スプレッドシートに保存（env方式）

import os
import json
import gspread
from google.oauth2.service_account import Credentials


def get_client():
    service_account_info = json.loads(
        os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    )

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        service_account_info,
        scopes=scopes
    )

    return gspread.authorize(creds)


def save_result(level, score):
    client = get_client()
    sheet = client.open("tanin_diagnosis_logs").sheet1
    sheet.append_row([level, score])
