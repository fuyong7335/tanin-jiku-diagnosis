# diagnosis/logic.py
# 役割：合計スコアからタイプ判定し、診断結果メッセージを組み立てる

import random

# ── 区切り線の下に出す「止める文」 ──
STOP_MESSAGE = (
    "もう少し、言葉を受け取りたいと思われたら\n"
    "こちらからご連絡ください。\n\n"
    "1通のメールで、言葉をお返しします。"
)

MESSAGES = {
    "light": {
        "observation": [
            "今回の回答からは、判断の舵を内側に戻す力がすでにある様子が見えます。",
            "周囲を意識しながらも、自分の感覚を完全には失っていない状態です。"
        ],
        "mirror": [
            "ただ、忙しさが続くと、無意識に外側へ寄る場面もありそうです。",
            "合わせることが増えすぎていないか、少し立ち止まってみてもよいかもしれません。"
        ],
        "question": [
            "最近、自分の感覚を優先できたのはどんな場面でしたか？",
            "そのとき、何が判断の支えになっていましたか？"
        ]
    },

    "middle": {
        "observation": [
            "今回の回答は、自分軸と他人軸が場面ごとに入れ替わる傾向を示しています。",
            "普段は保てていても、負荷がかかると外側に寄りやすい状態です。"
        ],
        "mirror": [
            "期待に応えようとする気持ちが、判断の前に立つことがありそうです。",
            "正解を探すほど、選択が重くなっていないでしょうか。"
        ],
        "question": [
            "外側に寄り始める合図は、あなたの場合どれでしょうか？",
            "最近、自分の感覚を後回しにした回数は増えていますか？"
        ]
    },

    "strong": {
        "observation": [
            "今回の回答からは、判断の舵が外側に置かれている時間が長い傾向が見えます。",
            "自分で決めているつもりでも、反応に引っ張られやすい状態かもしれません。"
        ],
        "mirror": [
            "周囲を優先することで、自分を守ってきた時間が長かった可能性があります。",
            "もし反応が消えたら、判断の感触は大きく変わるかもしれません。"
        ],
        "question": [
            "あなたの判断は、普段どこから許可を得ていますか？",
            "反応がなくなったとしたら、選択はどう変わりそうでしょうか？"
        ]
    }
}

def get_level(score):
    if score >= 22:
        return "strong"
    elif score >= 14:
        return "middle"
    else:
        return "light"

def build_message(score):
    level = get_level(score)
    data = MESSAGES[level]

    return {
        "level": level,
        "observation": random.choice(data["observation"]),
        "mirror": random.choice(data["mirror"]),
        "question": random.choice(data["question"]),
        "stop": STOP_MESSAGE
    }
