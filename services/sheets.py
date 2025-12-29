# services/sheets.py
import os
import json
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials


def get_client():
    service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
    return gspread.authorize(creds)


def save_message(level: str, score: str, message: str):
    client = get_client()

    sheet_key = os.environ["SPREADSHEET_KEY"]  # Renderの環境変数に入れる
    sheet = client.open_by_key(sheet_key).sheet1

    timestamp = datetime.now().isoformat(timespec="seconds")

    sheet.append_row([timestamp, level, score, message])
