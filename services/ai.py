import os
from openai import OpenAI

def generate_diagnosis_text(*, score: int, highlights: list[str]) -> str:
    """
    score: 合計スコア
    highlights: 高め回答の質問文（最大3つ）
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # APIキーがない時の保険（アプリが落ちないようにする）
        # ※ここはAIなしでも動くように「最低限」返す
        lines = [
            "今の回答には、「人の目や空気で判断が揺れやすい場面」が含まれていました。",
            "それは弱さではなく、今までそうせざるを得なかった癖かもしれません。",
            "でも最後に選ぶのは、いつもあなたです。",
            "思い当たる場面が、ひとつでも浮かびますか？",
        ]
        return "\n".join(lines)

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    highlights_text = "\n".join([f"- {h}" for h in highlights]) if highlights else "- （特に強い項目は抽出なし）"

    system = (
        "あなたは日本語の文章作成者。読者を誘導せず、命令せず、一般論に逃げず、短く刺さる言葉を作る。"
        "心理学者っぽい説明口調は避け、日常語で。断定しすぎず「〜かもしれません」を基本にする。"
        "出力はラベル無し・箇条書き無し・4〜6行。途中に一度だけ、短くビシッとした一文を入れる。"
        "（例：『選ぶのはあなたです。』のように）"
    )

    user = (
        "以下は自己理解（他人軸）診断の回答傾向です。\n"
        f"合計スコア: {score}\n"
        "高め回答の設問（抜粋）:\n"
        f"{highlights_text}\n\n"
        "この情報だけで、読み手が『あ、これ私かも』と思える短い結果文を作ってください。"
        "話が飛ばないように、自然な流れで。"
    )

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.7,
    )

    text = (resp.choices[0].message.content or "").strip()
    # 念のため空対策
    return text if text else "今の回答には、判断が外側に寄りやすい場面が含まれていました。\n選ぶのはあなたです。\n思い当たる場面が浮かびますか？"
