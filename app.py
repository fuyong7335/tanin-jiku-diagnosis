# app.py
import os
import uuid
from flask import Flask, render_template, request

from diagnosis.questions import QUESTIONS
from diagnosis.logic import build_message
from services.sheets import save_result, save_memo  # sheets側に用意する

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        # ① 回答を QUESTIONS 基準で集める（←ここが重要）
        answers = []
        for q in QUESTIONS:
            v = int(request.form.get(f"answer{q.id}", "0"))
            answers.append((q, v))

        total_score = sum(v for _, v in answers)

        # ② 強めに反応した質問（上位3つ）を AI に渡す
        highlights = [q.text for (q, v) in answers if v >= 3][:3]

        # ③ AIメッセージ生成（logic.py 側でAI呼び出し）
        result = build_message(total_score, highlights=highlights)

        # ④ スプシにログ（必要な列だけ）
        session_id = str(uuid.uuid4())
        save_result(session_id=session_id, score=total_score)

        return render_template(
            "result.html",
            result=result,
            score=total_score,
            session_id=session_id,
            memo_saved=False
        )

    return render_template("form.html", questions=QUESTIONS)

@app.route("/memo", methods=["POST"])
def memo():
    session_id = request.form.get("session_id", "")
    score = int(request.form.get("score", "0"))
    memo_text = (request.form.get("memo") or "").strip()

    # 空は保存しない（ありがとう表示もしない）
    if memo_text:
        save_memo(session_id=session_id, score=score, memo=memo_text)

    # もう一回結果ページを再表示（保存メッセージだけ出す）
    highlights = []  # 再生成時に必要なら session に持たせる。今は空でOK
    result = build_message(score, highlights=highlights)

    return render_template(
        "result.html",
        result=result,
        score=score,
        session_id=session_id,
        memo_saved=bool(memo_text)
    )

if __name__ == "__main__":
    app.run(debug=True)
