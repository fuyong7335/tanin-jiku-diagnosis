# services/ai.py
import os
from openai import OpenAI


def _safe_get_output_text(resp) -> str:
    # responses API: resp.output_text が基本
    if hasattr(resp, "output_text") and resp.output_text:
        return resp.output_text.strip()
    # 念のため
    try:
        return resp.output[0].content[0].text.strip()
    except Exception:
        return ""


def generate_diagnosis_text(score: int, level: str, highlights: list[str]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # キー無しなら落とさず、短い固定文で返す（起動安定優先）
        return (
            "いくつかの回答で、相手の反応を先に考えてしまう傾向が出ています。\n"
            "続くと自分の本音が後ろに回りやすくなります。\n"
            "選ぶのはあなた。決めるのもあなた。答えはいつも、あなたの中にあります。"
        )

    client = OpenAI(api_key=api_key)

    # AIに渡す材料（高かった質問だけ）
    highlight_text = "\n".join([f"- {t}" for t in highlights]) if highlights else "-（特に強い項目は少なめ）"

    system = (
        "あなたは日本語の文章が上手い編集者です。"
        "医療・心理の診断はしません。断定しません。"
        "見出し（例：観察/鏡/問い）やラベルは一切書きません。"
        "出力は4〜6行。1行は短め。読みやすい自然な日本語。"
        "文章は『あなたは〜傾向があります／かもしれません』の口調で、説明臭くしない。"
        "少し厳しさはあってよいが、責めない。"
        "必ず1回だけ次の一文をそのまま入れる："
        "『選ぶのはあなた。決めるのもあなた。答えはいつも、あなたの中にあります。』"
    )

    user = f"""
これは他人軸傾向を“自分で気づく”ための短い結果文です。
スコア: {score}（内部用）
強く出た項目（質問文）:
{highlight_text}

条件:
- 見出し禁止、ラベル禁止
- 4〜6行
- 最後は問いで締める（短く）
- 「他人軸」という単語を連発しない（使うなら1回まで）
"""

    resp = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_output_tokens=240,
    )

    text = _safe_get_output_text(resp)
    # 空で返ってきたときの保険
    return text or (
        "いくつかの回答で、相手の反応を先に考えてしまう傾向が出ています。\n"
        "続くと自分の本音が後ろに回りやすくなります。\n"
        "選ぶのはあなた。決めるのもあなた。答えはいつも、あなたの中にあります。\n"
        "今、いちばん引っかかっている場面はどれですか？"
    )
