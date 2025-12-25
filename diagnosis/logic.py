# diagnosis/logic.py
import random

STOP_MESSAGE = (
    "もう少し言葉を受け取りたいと思われたら、\n"
    "こちらからご連絡ください。1通のメールで返信をお返しします。\n"
)

MESSAGES = {
    "light": {
        "observation": [
            "普段は自分の感覚で決められることが多いようです。",
            "大切なところで自分を優先できる力が見えます。"
        ],
        "mirror": [
            "ただ、忙しいとつい人に合わせてしまうことがあるかもしれません。",
            "疲れや不安があると判断が他人基準に傾きやすい傾向があります。"
        ],
        "lead": [
            "物事を自分で決められているとき、何が支えになっていますか？",
            "その選択のとき、どんな気持ちがありましたか？"
        ],
        "question": [
            "そのことに気づいていますか？",
            "普段は何があなたを支えていますか？"
        ]
    },
    "middle": {
        "observation": [
            "普段は自分で決めている場面もありますが、場面によって人に合わせがちです。",
            "時々、判断の軸が外に引っ張られる瞬間があるようです。"
        ],
        "mirror": [
            "期待に応えようとする気持ちが、先に立つことがあるかもしれません。",
            "『正しい言い方』を探すうちに、本音が遅れてしまうことがありそうです。"
        ],
        "lead": [
            "外側に寄り始める時、まずどんな感覚が出ますか？",
            "その時、体や呼吸に変化はありませんか？"
        ],
        "question": [
            "そのことに気づいていますか？",
            "最近、それが増えていませんか？"
        ]
    },
    "strong": {
        "observation": [
            "判断の舵が外側に置かれている時間が長いように見えます。",
            "反応で決めてしまう瞬間が多くなっているかもしれません。"
        ],
        "mirror": [
            "周囲を優先してきた分、自分の声が聞こえにくくなっている可能性があります。",
            "『もし誰にも迷惑をかけなくていい』と考えるのが難しいことはありませんか？"
        ],
        "lead": [
            "あなたの判断は普段どこから来ていますか？（誰／空気／正しさ など）",
            "その状態はいつ頃から続いていますか？"
        ],
        "question": [
            "そのことに気づいていますか？",
            "それに気づいたとき、何が変わりそうですか？"
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
        "lead": random.choice(data["lead"]),
        "question": random.choice(data["question"]),
        "stop": STOP_MESSAGE
    }
