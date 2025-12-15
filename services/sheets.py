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
    sheet = client.open_by_key("1f9nZ2SW43Q86UEH1hiAeAn10ZNf-jYWfiQbl65SB2C0").sheet1
    sheet.append_row([level, score])

