# diagnosis/logic.py
import random
STOP_MESSAGE = (
    "もぅ少し、言葉を受け取りたいと思われたら\n"
    "必要な方にだけ、1通のみメールで言葉をお返しします。\n"
    "
)
# --- メッセージ素材（例） ---
MESSAGES = {
    "light": {
        "observation": [
            "普段は自分の感覚で決められることが多いようです。",
            "周囲を気にしつつも、自分の判断を保てる場面が増えています。"
        ],
        "mirror": [
            "ただ、忙しいときはつい人に合わせてしまうことがあるようです。",
            "疲れていると、安全な選択を優先しやすくなるかもしれません。"
        ],
        "lead": [
            "普段そうできている理由は何だと思いますか？",
            "そのとき、どんなことが支えになっていましたか？"
        ],
        "question": [
            "そのことに気付いていますか？",
            "それを続けることで得ているものは何ですか？"
        ]
    },

    "middle": {
        "observation": [
            "状況によって自分軸と他人軸が入れ替わる傾向が見られます。",
            "普段は自分の感覚でできても、負荷で外側に寄りやすいタイプです。"
        ],
        "mirror": [
            "期待に応えることが先に来て、あとで疲れが出ることがあるかもしれません。",
            "『正しい言い方』を探してしまい、本音が遅れる場面があるようです。"
        ],
        "lead": [
            "その合図に気づいたら、まず何をしますか？",
            "最近、無理をしていませんか？"
        ],
        "question": [
            "そのことに気付いていますか？",
            "気づいた後にいつも取る行動は何ですか？"
        ]
    },

    "strong": {
        "observation": [
            "判断の舵が外側に置かれている時間が長く見えます。",
            "他人の反応で判断が左右されやすい状態かもしれません。"
        ],
        "mirror": [
            "『誰にも迷惑をかけたくない』という信念が強く働いている可能性があります。",
            "自分の感覚を見ないで過ごしてきた期間が長いのかもしれません。"
        ],
        "lead": [
            "まず小さな一歩として、今日は何を選べそうですか？",
            "その選択であなたが守れるものは何ですか？"
        ],
        "question": [
            "そのことに気付いていますか？",
            "いつ頃からそう感じ始めましたか？"
        ]
    }
}

# レベル判定
def get_level(score):
    if score >= 22:
        return "strong"
    elif score >= 14:
        return "middle"
    else:
        return "light"

# build_message: return のキーはテンプレートと一致させること
def build_message(score):
    level = get_level(score)
    data = MESSAGES[level]

    return {
        "level": level,
        "observation": random.choice(data["observation"]),
        "mirror": random.choice(data["mirror"]),
        "lead": random.choice(data["lead"]),       # 新規導線／誘導文（短め）
        "question": random.choice(data["question"])
    }
