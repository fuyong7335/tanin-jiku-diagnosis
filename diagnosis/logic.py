# diagnosis/logic.py
from typing import List, Dict
from services.ai import generate_diagnosis_text

CTA_TEXT = (
    "ひとことメモ（匿名）を残せます。\n"
    "返事はいりません。1行でも大丈夫です。\n"
    "※個人が特定される情報は書かないでください。"
)

def get_level(score: int) -> str:
    if score >= 22:
        return "strong"
    elif score >= 14:
        return "middle"
    return "light"

def build_message(score: int, highlights: List[str] | None = None) -> Dict:
    level = get_level(score)
    highlights = highlights or []

    # AIに渡す材料（短く・具体）
    text = generate_diagnosis_text(score=score, level=level, highlights=highlights)

    return {
        "level": level,     # 内部用（テンプレで出さない）
        "text": text,       # result.html はこれを表示
        "cta": CTA_TEXT
    }
