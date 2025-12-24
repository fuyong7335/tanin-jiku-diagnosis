# diagnosis/logic.py
import random

# ===== 止め文（最小）=====
STOP_MESSAGE = (
    "もう少し、言葉を受け取りたいと思われたら\n"
    "こちらからご連絡ください。\n"
    "1通のメールで、言葉をお返しします。"
)

# ===== 診断メッセージ =====
MESSAGES = {
    "light": {
        "observation": [
            "今回の回答からは、他人の影響を受けつつも、自分の感覚を取り戻せている様子が見えます。",
            "完全に他人軸ではなく、自分で選び直せる力が残っている状態です。"
        ],
        "mirror": [
            "ただ、忙しさや疲れが重なると、人に合わせる選択が増えやすい傾向もありそうです。",
            "「まあいいか」と流したあとに、少し疲れが残ることはありませんか。"
        ],
        "question": [
            "最近、「本当はどうしたかった？」と立ち止まれた場面はありましたか？"
        ]
    },

    "middle": {
        "observation": [
            "今回の回答は、判断の基準が自分よりも周囲に寄りやすい状態を示しています。",
            "自分で決めているつもりでも、他人の反応が判断に影響しやすいようです。"
        ],
        "mirror": [
            "期待に応えようとする気持ちが先に立ち、自分の本音が後回しになることがありそうです。",
            "選んだあとに「これでよかったのかな」と考え直すことはありませんか。"
        ],
        "question": [
            "その選択は、「納得」からでしたか？それとも「波風を立てないため」でしたか？"
        ]
    },

    "strong": {
        "observation": [
            "今回の回答は、判断の軸がほとんど外側に置かれている状態を示しています。",
            "自分の気持ちよりも、相手や場の反応を優先する時間が長かったのかもしれません。"
        ],
        "mirror": [
            "合わせることで関係は保てても、安心や満足が増えにくい状態が続いていそうです。",
            "「自分はどうしたいか」を考える余裕がなくなっていませんか。"
        ],
        "question": [
            "もし誰の反応も気にしなくていいとしたら、今とは違う選択になりますか？"
        ]
    }
}

# ===== 判定 =====
def get_level(score):
    if score >= 22:
        return "strong"
    elif score >= 14:
        return "middle"
    else:
        return "light"

# ===== 結果組み立て（固定）=====
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
