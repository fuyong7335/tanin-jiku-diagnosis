import random

MESSAGES = {
    "light": {
        "title": "あなたの傾向：外側に寄りすぎないタイプ",
        "observations": [
            "全体として、判断の軸を内側に戻せる場面が多いようです。",
            "周りを見ながらも、自分の感覚を見失いにくい傾向が出ています。"
        ],
        "mirrors": [
            "ただ、忙しさや気疲れが重なると、反射的に合わせにいく瞬間も増えやすいです。",
            "「合わせるのが速い」日は、あとから疲れが残りやすいかもしれません。"
        ],
        "questions": [
            "最近、合わせたあとに疲れた出来事はありましたか？",
            "内側に戻せている時、何が支えになっていますか？"
        ],
    },
    "middle": {
        "title": "あなたの傾向：場面によって外側に寄りやすいタイプ",
        "observations": [
            "普段は保てても、緊張や忙しさで判断が外側に寄りやすいようです。",
            "空気を読む力が強く、その分、本音が後ろに下がりやすい傾向が出ています。"
        ],
        "mirrors": [
            "「正解探し」が始まると、自分の感覚が小さくなることがあります。",
            "無理の自覚が遅れて、あとからどっと疲れる流れになりやすいかもしれません。"
        ],
        "questions": [
            "外側に寄り始める“最初の合図”は、あなたの場合どれですか？",
            "最近、自分の感覚を置き去りにした回数は増えていますか？"
        ],
    },
    "strong": {
        "title": "あなたの傾向：外側に引っぱられやすい時間が長いタイプ",
        "observations": [
            "判断が外側に引っぱられやすい状態が続いているサインが出ています。",
            "自分で決めたはずでも、相手の反応で揺れやすい傾向が見えます。"
        ],
        "mirrors": [
            "これは弱さではなく、そうする必要があった時間が長かった可能性もあります。",
            "自分の気持ちを見る前に、“波風が立たない方”へ体が動いてしまうことがあるかもしれません。"
        ],
        "questions": [
            "あなたの「許可」は、普段どこから出ていますか？（誰／空気／正しさ）",
            "もし反応が消えたら、あなたの選択はどこが変わりますか？"
        ],
    },
}

def get_level(score: int) -> str:
    if score >= 22:
        return "strong"
    if score >= 14:
        return "middle"
    return "light"

def build_message(score: int) -> dict:
    level = get_level(score)
    data = MESSAGES[level]
    return {
        "level": level,
        "title": data["title"],
        "observation": random.choice(data["observations"]),
        "mirror": random.choice(data["mirrors"]),
        "question": random.choice(data["questions"]),
    }
