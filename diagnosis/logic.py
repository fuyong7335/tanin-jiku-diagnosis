# diagnosis/logic.py
import random
from services.ai import generate_text

# 返信なし版：結果ページの下に出す固定文（あなたのKindle文に寄せた）
CTA_TEXT = (
    "診断結果の最後に、「ひとことメモ（匿名）」を残せる欄があります。\n"
    "返事はいりません。1行でも大丈夫です。\n"
    "いただいた言葉は、今後の改善や発信の参考にします。\n"
    "※氏名やメールなど、個人が特定される情報は書かないでください。\n"
    "※返信は行っていません。"
)

def get_level(score: int) -> str:
    # ※レベルは内部判定用（画面に出さない前提）
    if score >= 22:
        return "strong"
    elif score >= 14:
        return "middle"
    else:
        return "light"

def build_prompt(answers: list[int], score: int) -> str:
    """
    answers: 1〜5 の数値が 10個想定（あなたの質問数に合わせてOK）
    """
    level = get_level(score)

    # AIに“逃げ道”を与えないための制約（ここがキモ）
    # ・見出し禁止
    # ・専門用語や比喩（舵など）禁止
    # ・短く（4〜6行）
    # ・一言だけ“ビシッと”入れる
    # ・断定しすぎない（〜かもしれません／〜の傾向）
    constraints = f"""
あなたは「他人軸（他人の反応が気になり、自分の判断が揺れる）」をテーマに、診断結果の短い文章を作る書き手です。
次の制約を必ず守ってください。

【制約】
- 日本語、やさしい日常語だけ（専門用語・比喩・抽象語を避ける）
- 見出し語（例：観察/鏡/問い/判定/Strong/Middle など）を一切書かない
- 4〜6行。1行は短め。説明っぽくしない
- 「〜しがち」「〜の傾向」「〜かもしれません」で書く（決めつけない）
- どこか1行だけ、短く強い言葉を入れる：
  「選ぶのはあなた。答えもあなたの中にある。」
- 最後は質問で終える（例：「今、何を優先したいですか？」）
- 医療・心理の診断のような言い方はしない

【参考（他人軸の例）】
- 相手の顔色や反応が気になって決めにくい
- 断る前に相手の反応を想像してしまう
- 後から「これでよかったかな」が残る

【入力】
スコア: {score}
内部レベル: {level}
回答（1〜5）: {answers}
""".strip()

    return constraints

def build_message(answers: list[int], score: int) -> dict:
    prompt = build_prompt(answers, score)

    # 生成に失敗したら “最低限の保険文” を返す（アプリを落とさない）
    try:
        text = generate_text(prompt)
        if not text:
            raise RuntimeError("empty ai text")
    except Exception:
        level = get_level(score)
        # フォールバック（短く、頭に入る言葉）
        if level == "strong":
            text = (
                "人の反応が気になって、決める前に心が揺れやすい状態かもしれません。\n"
                "その分、自分の本音が後回しになりがちです。\n"
                "選ぶのはあなた。答えもあなたの中にある。\n"
                "いま本当は、何を優先したいですか？"
            )
        elif level == "middle":
            text = (
                "自分で決めたいのに、最後に相手の反応が気になりやすい傾向がありそうです。\n"
                "決めたあとに「これでよかったかな」が残りやすいかもしれません。\n"
                "選ぶのはあなた。答えもあなたの中にある。\n"
                "いま本当は、何を優先したいですか？"
            )
        else:
            text = (
                "ふだんは自分の感覚で決められることが多いのかもしれません。\n"
                "ただ、忙しい時だけ人に合わせて決めてしまう場面がありそうです。\n"
                "選ぶのはあなた。答えもあなたの中にある。\n"
                "最近いちばん、自分を後回しにしたのはいつですか？"
            )

    return {
        "text": text,
        "cta": CTA_TEXT,
        "level": get_level(score),  # 内部用（画面で使わないならOK）
    }
