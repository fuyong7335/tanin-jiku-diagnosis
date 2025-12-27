# services/sheets.py
import os
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timezone, timedelta

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SPREADSHEET_KEY = os.environ.get("SPREADSHEET_KEY")  # なくても動くよう後で直す

def get_client():
    info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
    creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    return gspread.authorize(creds)

def append_log_row(timestamp, email, level, score):
    """
    app.py が import する想定の関数名。
    シートの列: timestamp, email, level, score
    """
    client = get_client()

    # SPREADSHEET_KEY を env に入れてるならそれを使う
    if SPREADSHEET_KEY:
        sheet = client.open_by_key(SPREADSHEET_KEY).sheet1
    else:
        # ここはあなたのキーを直書きしてるならそのままでもOK
        sheet = client.open_by_key("1f9nZ2SW43Q86UEH1hiAeAn10ZNf-jYWfiQbl65SB2C0").sheet1

    sheet.append_row([timestamp, email, level, score], value_input_option="USER_ENTERED")

def jst_now_str():
    JST = timezone(timedelta(hours=9))
    return datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")
