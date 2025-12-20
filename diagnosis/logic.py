# diagnosis/logic.py
import random

MESSAGES = {
    "light": {
        "observations": [
            "人の気持ちを大切にしながらも、自分の感覚を見失わずにいられる場面が増えてきています。"
        ],
        "needles": [
            "ただ、そのバランスは無意識のうちに崩れやすいものでもあります。"
        ],
        "questions": [
            "最近、自分の気持ちをそのまま選択できた場面はありましたか？"
        ],
        "cta": ""
    },
    "middle": {
        "observations": [
            "人の期待を感じ取る力が高く、その分、自分の本音を後回しにしてきたようです。"
        ],
        "needles": [
            "それは優しさであると同時に、無理の積み重ねでもあります。"
        ],
        "questions": [
            "本当は断りたかったのに、引き受けたことはありませんか？"
        ],
        "cta": ""
    },
    "strong": {
        "observations": [
            "これまで自分を後回しにして生きてくる必要があった状況があったように感じます。"
        ],
        "needles": [
            "『もし誰にも迷惑をかけなくていいとしたら』という問いが、浮かばなかったとしたら。"
        ],
        "questions": [
            "自分の気持ちを考えること自体を、避けてきたことはありませんか？"
        ],
        "cta": (
            "この問いを、今日はひとりで抱えなくてもいいと思えたら、"
            "一通だけ、言葉を置きに来てください。\n\n"
            "このやり取りは、あなたからの一通に、私が一通お返しする形で終わります。\n\n"
            "※このやり取りは有料です。"
        )
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
        "observation": random.choice(data["observations"]),
        "needle": random.choice(data["needles"]),
        "question": random.choice(data["questions"]),
        "cta": data["cta"]
    }
