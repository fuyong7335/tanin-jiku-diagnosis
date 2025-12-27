# services/ai.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
あなたは日本語の文章作成者です。
ユーザーの診断回答（文章の断片）を材料に、短く自然な日本語で結果メッセージを書きます。

制約:
- 見出し（観察/鏡/問い/判定など）を出さない
- 「今回の回答は」「傾向を示しています」など説明っぽい言い回しは避ける
- 「舵」「外側/内側」など抽象メタファーは使わない
- 4〜6行の短文（スマホで読みやすく）
- 1行だけ、芯のある言葉を入れる（例: 選ぶのはあなた。答えはあなたの中にある。）
- 断定しすぎない（〜かもしれません／〜になりやすい）
"""

def generate_result_text(score: int, highlights_text: str) -> str:
    # highlights_text は「強く出た回答（質問文）」の短い抜粋が入る想定
    user_prompt = f"""
スコア: {score}

強く出た要素（抜粋）:
{highlights_text}

この材料を使って、結果メッセージを4〜6行で作ってください。
"""

    # OpenAI公式の Python SDK は responses.create / output_text が使えます
    # （platform.openai.com のドキュメント例と同じ形）
    resp = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_output_tokens=220,
    )
    return (resp.output_text or "").strip()
