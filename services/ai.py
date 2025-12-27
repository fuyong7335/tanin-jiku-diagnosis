# services/ai.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 必要なら Render の環境変数で OPENAI_MODEL を変えられるようにしておく
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.2")

def generate_result_text(score: int, answers: list[int]) -> str:
    """
    10問の回答（0-4 or 1-5など）と合計スコアから、結果メッセージ本文だけ返す
    ※ラベル（観察/鏡など）絶対出さない
    """
    # ここはあなたの採点に合わせて調整（例）
    if score >= 22:
        level = "strong"
    elif score >= 14:
        level = "middle"
    else:
        level = "light"

    prompt = f"""
あなたは「他人軸チェック」の結果文を作る編集者です。
以下の条件を厳守して、日本語で短く書いてください。

【絶対ルール】
- 断定しない（〜の傾向/〜しやすい/〜かもしれません）
- 心理診断・医療っぽい表現は禁止
- 「観察」「鏡」「問い」などの見出し語は一切出さない
- 一般論・自己啓発っぽいテンプレは禁止（ふわっと褒めない）
- 回答にない事実を作らない（ハルシネーション禁止）
- 全体は4〜6行。1行は短め。読み疲れさせない

【入れてほしい“ビシッと1行”】【必須】
- 「選ぶのも、決めるのも、あなたです。」（この文はそのまま入れる）

【入力】
- 判定レベル（内部用）: {level}
- 合計スコア: {score}
- 回答の点数配列: {answers}

では、結果メッセージ本文だけを書いてください。
""".strip()

    res = client.responses.create(
        model=MODEL,
        input=prompt,
    )

    return (res.output_text or "").strip()
