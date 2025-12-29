# diagnosis/logic.py
import random

FIXED_STOPPER = """ここから先は、
決まった文章ではうまくお返しできません。

感じている思いは
同じかもしれない。
ただ、
それをどう言葉にするかは
人それぞれだからです。

だから、
あなたが今、
自分の思いをどう感じているのかを
あなた自身の言葉で置いてもらってから、
初めて見えてくるものがあります。

（送らなくても、診断はここで完了です）"""

MESSAGES = {
    "light": {
        "title": "他人軸度：軽め",
        "observations": [
            "今回の回答は、「舵を内側に戻す力がすでにある」傾向を示しています。",
            "外側に寄る瞬間はあっても、戻れる地点を持っているタイプです。",
        ],
        "mirror": [
            "ただ、忙しさや責任が増えるほど、判断が“反射”になりやすいところも見えます。",
            "人に合わせられる分、疲れに気づくのが少し遅れる場面があるかもしれません。",
        ],
        "questions": [
            "内側に戻せている時、何が支えになっていますか？",
            "外側に寄る時、決まって増えるものは何ですか？（焦り／比較／責任感 など）",
        ],
    },
    "middle": {
        "title": "他人軸度：中くらい",
        "observations": [
            "今回の回答は、「自分軸と他人軸が場面で入れ替わる」傾向を示しています。",
            "普段は保てても、緊張や忙しさで外側に寄りやすいタイプです。",
        ],
        "mirror": [
            "迷うほど“正解探し”が増えて、本音が後回しになりやすい流れが出ています。",
            "無理の自覚が遅れて、後からどっと疲れが来る形になりやすいかもしれません。",
        ],
        "questions": [
            "外側に寄り始める“最初の合図”は、あなたの場合どれですか？",
            "「自分の感覚」を無視した回数は、最近増えていますか？",
        ],
    },
    "strong": {
        "title": "他人軸度：強め",
        "observations": [
            "今回の回答は、「舵が外側に置かれている時間が長い」傾向を示しています。",
            "自分で決めているつもりでも、最終判断が“反応”に引っ張られやすい状態です。",
        ],
        "mirror": [
            "相手の表情や間で、自分の判断が揺れる流れが出やすいかもしれません。",
            "“正しい言い方”を探している間に、本音が遅れてしまうことはありませんか。",
        ],
        "questions": [
            "あなたの「許可」は、普段どこから出ていますか？（誰／空気／正しさ）",
            "もし反応が消えたら、あなたの選択はどこが変わりますか？",
        ],
    },
}


def get_level(score: int) -> str:
    # 10問×1〜5点 → 10〜50点
    if score >= 38:
        return "strong"
    elif score >= 28:
        return "middle"
    else:
        return "light"


def build_message(score: int) -> dict:
    level = get_level(score)
    data = MESSAGES[level]

    return {
        "level": level,
        "title": data["title"],
        "observation": random.choice(data["observations"]),
        "mirror": random.choice(data["mirror"]),
        "question": random.choice(data["questions"]),
        "stopper": FIXED_STOPPER,
    }
