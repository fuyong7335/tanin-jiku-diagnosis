# services/sheets.py
import os
import json
from datetime import datetime, timezone, timedelta

import gspread
from google.oauth2.service_account import Credentials

JST = timezone(timedelta(hours=9))

# 既存のキーを使う（必要なら Render の環境変数で上書き可能）
DEFAULT_SHEET_KEY = "1f9nZ2SW43Q86UEH1hiAeAn10ZNf-jYWfiQbl65SB2C0"


def get_client():
    # Render環境変数：GOOGLE_SERVICE_ACCOUNT_JSON に、サービスアカウントJSON全文を入れる想定
    raw = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not raw:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON is not set")

    info = json.loads(raw)
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    return gspread.authorize(creds)


def _get_ws(spreadsheet, title: str):
    try:
        return spreadsheet.worksheet(title)
    except Exception:
        # 無ければ作る
        return spreadsheet.add_worksheet(title=title, rows=1000, cols=20)


def append_result_row(score: int, highlights: list[str], ai_text: str):
    client = get_client()
    sheet_key = os.getenv("SHEET_KEY", DEFAULT_SHEET_KEY)
    ss = client.open_by_key(sheet_key)

    ws = _get_ws(ss, "results")  # ここに結果
    timestamp = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")

    ws.append_row([
        timestamp,
        score,
        " / ".join(highlights),
        ai_text
    ])


def append_memo_row(score: int, memo: str):
    client = get_client()
    sheet_key = os.getenv("SHEET_KEY", DEFAULT_SHEET_KEY)
    ss = client.open_by_key(sheet_key)

    ws = _get_ws(ss, "memo")  # ここに匿名メモ
    timestamp = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")

    ws.append_row([
        timestamp,
        score,
        memo
    ])
