# diagnosis/logic.py
import random

# 固定の止め文（短く・明確）
STOP_MESSAGE = (
    "もう少し言葉を受け取りたいと思ったら、こちらからご連絡ください。\n"
    "1通のメールで返信をお返しします。"
)

MESSAGES = {
    "light": {
        "observation": [
            "普段は自分の感覚で決められることが多いようです。",
            "日常では自分の声を聞き取れている場面が増えています。"
        ],
        "mirror": [
            "ただ、忙しいとつい人に合わせてしまうことがあります。",
            "気づかないうちに“合わせる選択”が増えていないですか。"
        ],
        "question": [
            "そのことに気付いていますか？"
        ]
    },
    "middle": {
        "observation": [
            "場面によって自分より相手を優先しやすい傾向があります。",
            "普段は大丈夫でも、負荷がかかると外側に寄りやすいようです。"
        ],
        "mirror": [
            "期待に応えようとする気持ちが、あなたの判断を先にしているかもしれません。",
            "“正解を探す”クセが、決断を重くしていないでしょうか。"
        ],
        "question": [
            "そのことに気付いていますか？"
        ]
    },
    "strong": {
        "observation": [
            "多くの場面で相手の反応を優先してきた痕跡があります。",
            "自分で決めたつもりでも、反応に引っ張られていることが多いかもしれません。"
        ],
        "mirror": [
            "それは一種の安全策として身についてきた可能性があります。",
            "自分の欲求や違和感を抑えてきた時間が長かったのではないでしょうか。"
        ],
        "question": [
            "そのことに気付いていますか？"
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
        "question": data["question"][0],   # 常に同じ一文を返す
        "stop": STOP_MESSAGE
    }
