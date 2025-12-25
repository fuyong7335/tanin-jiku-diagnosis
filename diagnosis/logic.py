# diagnosis/logic.py
# 合計スコアから判定し、表示用の文章をランダムに組み立てて返すモジュール
# 配置場所: diagnosis/logic.py に置いてください

import random

# 結果画面の最後に出す案内（短く・明確に）
STOP_MESSAGE = (
    "もう少し言葉を受け取りたいと思われたら、こちらからご連絡ください。\n"
    "1通のメールで返信をお返しします。（任意）"
)

# 各レベルごとのメッセージ素材（短く日常語で分かりやすく）
MESSAGES = {
    "light": {
        "lead": [
            "普段は自分の感覚で決められることが多いようです。",
            "自分の判断で動けている場面がよく見られます。"
        ],
        "mirror": [
            "ただ、忙しいとつい人に合わせてしまうことがあります。",
            "疲れていると、知らず知らず“安全な選択”を優先してしまうことがあるかもしれません。"
        ],
        "question": [
            "そのことに気づいていますか？",
            "その場面に気づくことはできますか？"
        ]
    },
    "middle": {
        "lead": [
            "自分軸と他人軸が場面によって入れ替わる傾向があります。",
            "普段はできていても、負荷がかかると外側に引っ張られやすいようです。"
        ],
        "mirror": [
            "期待に応えようとする気持ちが、判断の前に立つことがありそうです。",
            "“正解探し”が増えると、決めることが重くなりやすいかもしれません。"
        ],
        "question": [
            "そのことに気づいていますか？",
            "そうした時、いつも何が先に出ますか？"
        ]
    },
    "strong": {
        "lead": [
            "判断の舵が外側に置かれている時間が長いように見えます。",
            "自分で決めているつもりでも、反応に引っ張られがちな状態かもしれません。"
        ],
        "mirror": [
            "周囲を優先してきたぶん、自分の声が聞こえにくくなっている可能性があります。",
            "『もし誰にも迷惑をかけなくていいとしたら』が想像しにくい状態かもしれません。"
        ],
        "question": [
            "そのことに気づいていますか？",
            "気づいたとき、何が少し変わりそうですか？"
        ]
    }
}

# スコアに応じた内部レベル判定（閾値は必要に応じて変更してください）
def get_level(score: int) -> str:
    if score >= 22:
        return "strong"
    elif score >= 14:
        return "middle"
    else:
        return "light"

# 外部表示用のラベル（日本語）
LEVEL_LABELS = {
    "light": "軽度",
    "middle": "中度",
    "strong": "重度"
}

# build_message: 呼び出し先（app.py やテンプレ）に渡す辞書を返す
def build_message(score: int) -> dict:
    level = get_level(score)
    data = MESSAGES[level]

    return {
        "level": level,                          # "light"/"middle"/"strong"（内部判定）
        "level_label": LEVEL_LABELS[level],      # 表示用ラベル（日本語）
        "lead": random.choice(data["lead"]),     # 結果の導入文（短め）
        "mirror": random.choice(data["mirror"]), # ちょっと厳しめの鏡（短め）
        "question": random.choice(data["question"]), # 表示用の問い（短く）
        "stop": STOP_MESSAGE                     # 最後の案内（固定）
    }
