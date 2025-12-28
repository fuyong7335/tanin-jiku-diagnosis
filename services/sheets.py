import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import gspread
from google.oauth2.service_account import Credentials

JST = ZoneInfo("Asia/Tokyo")

def _client():
    """
    Renderの環境変数 GOOGLE_SERVICE_ACCOUNT_JSON に
    サービスアカウントJSON（中身そのまま）を入れる想定。
    """
    raw = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not raw:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON が未設定です")

    info = json.loads(raw)
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    return gspread.authorize(creds)

def _sheet():
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not sheet_id:
        raise RuntimeError("GOOGLE_SHEET_ID が未設定です")
    return _client().open_by_key(sheet_id)

def _now_jst_str():
    return datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")

def append_result_row(*, score: int, highlights: list[str], ai_text: str):
    """
    Sheet1（1枚目）に保存
    A: timestamp(JST)
    B: score
    C: highlights(まとめ)
    D: ai_text
    """
    sh = _sheet()
    ws = sh.sheet1
    ws.append_row([
        _now_jst_str(),
        score,
        " / ".join(highlights) if highlights else "",
        ai_text,
    ], value_input_option="USER_ENTERED")

def append_memo_row(*, score: int, memo: str):
    """
    memo シートに保存（無ければ作る）
    A: timestamp(JST)
    B: score
    C: memo
    """
    sh = _sheet()
    try:
        ws = sh.worksheet("memo")
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title="memo", rows=1000, cols=10)
        ws.append_row(["timestamp", "score", "memo"], value_input_option="USER_ENTERED")

    ws.append_row([
        _now_jst_str(),
        score,
        memo,
    ], value_input_option="USER_ENTERED")
