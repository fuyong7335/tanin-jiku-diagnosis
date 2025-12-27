# services/sheets.py
import os
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timezone, timedelta

SPREADSHEET_KEY = "1f9nZ2SW43Q86UEH1hiAeAn10ZNf-jYWfiQbl65SB2C0"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def _now_jst() -> str:
    jst = timezone(timedelta(hours=9))
    return datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S")

def get_client():
    info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
    creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    return gspread.authorize(creds)

def _get_or_create_ws(spreadsheet, title: str, cols: int = 10):
    try:
        return spreadsheet.worksheet(title)
    except Exception:
        return spreadsheet.add_worksheet(title=title, rows=1000, cols=cols)

def save_diagnosis(session_id: str, score: int, answers: list[int], ai_text: str, level: str):
    client = get_client()
    ss = client.open_by_key(SPREADSHEET_KEY)
    ws = _get_or_create_ws(ss, "diagnosis", cols=8)

    ts = _now_jst()
    ws.append_row([
        ts,
        session_id,
        score,
        level,                 # 内部用（不要なら消してOK）
        json.dumps(answers, ensure_ascii=False),
        ai_text
    ])

def save_memo(session_id: str, score: str, memo: str):
    client = get_client()
    ss = client.open_by_key(SPREADSHEET_KEY)
    ws = _get_or_create_ws(ss, "memo", cols=6)

    ts = _now_jst()
    ws.append_row([
        ts,
        session_id,
        score,
        memo
    ])
