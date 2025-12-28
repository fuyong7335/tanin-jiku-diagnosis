from services.ai import generate_diagnosis_text

CTA_TEXT = (
    "もう少し言葉を受け取りたいと思われたらこちらからご連絡ください。\n"
    "1通のメールをお返しします。"
)
# ↑いまは「返信なし」運用なので、CTAは表示しないなら result.html側で出さないでもOK。
#   （この文はあなたの固定文として残しておけるように置いています）

def build_message(score: int, highlights: list[str]) -> dict:
    text = generate_diagnosis_text(score=score, highlights=highlights)
    return {
        "text": text,     # 画面に出す本文（AI）
        "cta": "",        # 返信なしなら空（表示しない）
    }
