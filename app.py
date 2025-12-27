# app.py
import logging
logging.basicConfig(level=logging.INFO)

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for

from diagnosis.questions import QUESTIONS
from diagnosis.logic import build_message, get_level
from services.sheets import append_log_row, append_memo_row

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        scores = []
        for key in request.form:
            if key.startswith("answer"):
                scores.append(int(request.form[key]))

        total_score = sum(scores)
        level = get_level(total_score)

        # AI診断文
        result = build_message(total_score, scores)

        # 個人情報なしログ保存
        append_log_row(level, total_score)

        logging.info(f"POST received score={total_score} level={level}")
        return render_template("result.html", result=result, score=total_score, level=level)

    return render_template("form.html", questions=QUESTIONS)

@app.route("/memo", methods=["POST"])
def memo():
    memo_text = (request.form.get("memo") or "").strip()
    level = request.form.get("level") or "unknown"
    score = int(request.form.get("score") or 0)

    # 空メモは保存しない（任意）
    if memo_text:
        append_memo_row(level, score, memo_text)

    return redirect(url_for("index"))
