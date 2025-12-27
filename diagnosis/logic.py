# diagnosis/logic.py
def get_level(score: int) -> str:
    if score >= 22:
        return "strong"
    elif score >= 14:
        return "middle"
    else:
        return "light"


CTA_TEXT = (
    "診断結果の最後に、「ひとことメモ（匿名）」を残せる欄があります。\n"
    "返事はいりません。１行でも大丈夫です。\n"
    "※氏名やメールなど、個人が特定される情報は書かないでください。"
)


def build_ai_prompt(score: int, answers: list[int]) -> tuple[str, str]:
    """
    return: (system_prompt, user_prompt)
    """
    level = get_level(score)

    system = (
        "あなたは文章が上手いカウンセラーではなく、"
        "読み手が自分で気づけるように言葉を置く編集者です。"
        "医療・診断・治療はしません。断定しません。脅しません。"
        "見出し（例：観察/鏡/問い）やラベルは出力しません。"
        "日本語は自然で、日常語を使います。"
        "出力は4〜6行。1行は短め。"
        "最後の1行だけ、少し厳しく『選ぶのは自分』をビシッと入れます。"
    )

    # levelごとの“方向性”だけ渡す（文章はAIが作る）
    if level == "light":
        hint = "普段は自分で決められるが、忙しいと合わせやすい。"
    elif level == "middle":
        hint = "自分で決めたいのに、相手の反応で揺れやすい。"
    else:
        hint = "相手優先が続き、自分の本音が後回しになりやすい。"

    user = (
        f"スコア: {score}\n"
        f"回答(1〜5): {answers}\n"
        f"傾向の方向性: {hint}\n\n"
        "この人が『あ、私のことだ』と思える自然な文章を4〜6行で。\n"
        "説明臭くしない。抽象語を避ける（例：舵/外側/内側 は使わない）。\n"
        "質問は入れてもいいが、1つまで。"
    )

    return system, user
