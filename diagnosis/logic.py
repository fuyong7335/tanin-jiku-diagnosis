# diagnosis/logic.py
from services.ai import generate_diagnosis_text

CTA_TEXT = (
    "診断結果の最後に、\n"
    "「ひとことメモ（匿名）」を残せる欄があります。\n"
    "返事はいりません。１行でも大丈夫です。\n"
    "いただいた言葉は、今後の改善や発信の参考にします。\n"
    "※氏名やメールなど、個人が特定される情報は書かないでください。\n"
    "※返信は行っていません。"
)

def get_level(score: int) -> str:
    # 内部用（画面には出さない）
    if score >= 22:
        return "strong"
    elif score >= 14:
        return "middle"
    return "light"


def build_message(score: int, highlights: list[str] | None = None) -> dict:
    highlights = highlights or []
    level = get_level(score)

    # AI本文（数行に収める）
    try:
        text = generate_diagnosis_text(score=score, level=level, highlights=highlights)
    except Exception:
        # 最低限のフォールバック（アプリを落とさない）
        text = (
            "いくつかの質問で、相手の反応を先に考えてしまう傾向が強めに出ています。\n"
            "それ自体は能力でもありますが、続くと自分の本音が後ろに回りやすくなります。\n"
            "選ぶのはあなた。決めるのもあなた。答えはいつも、あなたの中にあります。"
        )

    return {
        "text": text,
        "cta": CTA_TEXT,
        "level": level,   # 内部用（テンプレで表示しない）
        "score": score,   # 内部用
    }
