# diagnosis/logic.py
# 役割：合計スコアから傾向を出し、結果メッセージを組み立てる

import random

MESSAGES = {
    "light": {
        "title": "外に引っ張られにくい日が増えていそうです",
        "observations": [
            "今のところ、周りに合わせすぎて苦しくなる感じは強くは出ていません。",
            "空気を読みつつも、自分の感覚を戻せる場面がありそうです。"
        ],
        "mirror": [
            "ただ、忙しい時や疲れた時は、いつもより外側に寄りやすくなります。",
            "「大丈夫」って言いながら、気づかないうちに我慢が増えることもあります。"
        ],
        "questions": [
            "最近、「本当はこうしたい」が出た瞬間、どこで止めましたか？",
            "合わせた後に残る違和感は、どんな形で出やすいですか？"
        ],
    },

    "middle": {
        "title": "外の反応に寄りやすい場面がありそうです",
        "observations": [
            "普段は保てても、緊張や責任が増えると外側に寄りやすい雰囲気があります。",
            "考え方が丁寧なぶん、相手の反応を先に想像して動きやすいかもしれません。"
        ],
        "mirror": [
            "そのやり方は賢い反面、自分の本音が後ろに下がりやすいです。",
            "「ちゃんとしなきゃ」が増えるほど、選ぶのがしんどくなりがちです。"
        ],
        "questions": [
            "外側に寄り始める“最初の合図”は、あなたの場合どれですか？",
            "最近、「自分の感覚」を後回しにした回数は増えていませんか？"
        ],
    },

    "strong": {
        "title": "外の反応に引っ張られる時間が長かったのかもしれません",
        "observations": [
            "自分で決めているつもりでも、最後の一押しが“相手の反応”になりやすい雰囲気があります。",
            "安心のために合わせてきた時間が長かった可能性があります。"
        ],
        "mirror": [
            "ここが強い人ほど、頑張っているのに安心が増えにくいです。",
            "本音を出す前に、“正しい言い方”を探して止まってしまうことが起きやすいです。"
        ],
        "questions": [
            "「許可」が欲しくなる瞬間は、どんな場面で起きますか？",
            "もし相手の反応が消えたら、あなたの選択はどこが変わりますか？"
        ],
    },
}

def get_level(score: int) -> str:
    if score >= 22:
        return "strong"
    elif score >= 14:
        return "middle"
    else:
        return "light"

def build_message(score: int) -> dict:
    level = get_level(score)
    data = MESSAGES[level]

    return {
        "level": level,           # 内部処理用
        "title": data["title"],   # 表示用（断定を避けた）
        "observation": random.choice(data["observations"]),
        "mirror": random.choice(data["mirror"]),
        "question": random.choice(data["questions"]),
    }
