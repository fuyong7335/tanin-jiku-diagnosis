import os
from dataclasses import dataclass
from flask import Flask, render_template, request, redirect, url_for, session

from diagnosis.logic import build_message
from services.sheets import append_result_row, append_memo_row

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")  # Renderでは環境変数推奨

@dataclass
class Question:
    id: int
    text: str
    choices: list[tuple[str, int]]

CHOICES = [
    ("あてはまらない", 0),
    ("少しあてはまる", 1),
    ("あてはまる", 2),
    ("とてもあてはまる", 3),
]

# 本の導線に寄せた質問（例：10問）
QUESTIONS = [
    Question(1, "人からどう思われるかを、つい気にしてしまう。", CHOICES),
    Question(2, "決めるとき、自分の気持ちより相手の気持ちを優先しがちだ。", CHOICES),
    Question(3, "頼まれると断れないことが多い。", CHOICES),
    Question(4, "モヤモヤしても「気のせい」と自分に言い聞かせることがある。", CHOICES),
    Question(5, "誰かに迷惑をかけるのが怖い。", CHOICES),
    Question(6, "「ちゃんとしなきゃ」が頭の中で鳴りやすい。", CHOICES),
    Question(7, "本当はどうしたいのか、自分でも分からなくなる時がある。", CHOICES),
    Question(8, "人に嫌われたくない気持ちが強い。", CHOICES),
    Question(9, "相手に合わせすぎて、自分の意見を言えないことがある。", CHOICES),
    Question(10, "感情が揺れたとき、「私が悪いのかな」と思いやすい。", CHOICES),
]

@app.get("/")
def index():
    # ワンクッション（ここから開始）
    return render_template("index.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "GET":
        return render_template("form.html", questions=QUESTIONS)

    # POST：採点
    answers = []
    for q in QUESTIONS:
        v = int(request.form.get(f"answer{q.id}", "0"))
        answers.append((q, v))

    total_score = sum(v for _, v in answers)

    # 高め回答（3以上）を最大3つ抽出
    highlights = [q.text for (q, v) in answers if v >= 3][:3]

    # AI結果生成
    result = build_message(total_score, highlights)

    # スプシ保存（結果ログ）
    try:
        append_result_row(score=total_score, highlights=highlights, ai_text=result["text"])
    except Exception:
        # スプシが落ちても画面は出す（ユーザー体験優先）
        pass

    # resultをセッションに保存（/memo で再表示するため）
    session["score"] = total_score
    session["result_text"] = result["text"]

    return render_template(
        "result.html",
        result=result,
        score=total_score,
        memo_saved=False,
    )

@app.post("/memo")
def memo():
    memo_text = (request.form.get("memo") or "").strip()
    score = session.get("score", "")
    result_text = session.get("result_text", "")

    # 空メモは何もしないで結果へ戻す（Method Not Allowed回避＆UX）
    if not memo_text:
        return render_template(
            "result.html",
            result={"text": result_text, "cta": ""},
            score=score,
            memo_saved=False,
        )

    # 長すぎ対策
    if len(memo_text) > 500:
        memo_text = memo_text[:500]

    try:
        append_memo_row(score=int(score) if str(score).isdigit() else 0, memo=memo_text)
        saved = True
    except Exception:
        saved = False

    return render_template(
        "result.html",
        result={"text": result_text, "cta": ""},
        score=score,
        memo_saved=saved,
    )

if __name__ == "__main__":
    app.run(debug=True)
