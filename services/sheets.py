# services/sheets.py
import os
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from zoneinfo import ZoneInfo  # ★ JST(Asia/Tokyo)にする

SPREADSHEET_KEY = "1f9nZ2SW43Q86UEH1hiAeAn10ZNf-jYWfiQbl65SB2C0"

def get_client():
    service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
    return gspread.authorize(creds)

def save_result(email, level, score):
    try:
        client = get_client()
        sheet = client.open_by_key(SPREADSHEET_KEY).sheet1

        # ★ JSTでタイムスタンプ
        timestamp = datetime.now(ZoneInfo("Asia/Tokyo")).isoformat(timespec="seconds")

        sheet.append_row([timestamp, email, level, score])

    except Exception as e:
        print("=== SHEETS ERROR ===")
        print(e)
        raise
