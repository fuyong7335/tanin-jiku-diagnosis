# app.py
import os
import uuid
import logging
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()
logging.basicConfig(level=logging.INFO)

from diagnosis.questions import QUESTIONS
from diagnosis.logic import build_message, get_level  # get_levelは内部用
from services.sheets import append_log_row

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        try:
            # 回答スコア収集
            scores = []
            for q in QUESTIONS:
                v = request.form.get(f"answer{q['id']}")
                scores.append(int(v))

            total_score = sum(scores)
            level = get_level(total_score)  # 画面には出さない（内部用）
            session_id = str(uuid.uuid4())

            # AIで結果文章生成（失敗時はフォールバック）
            result_text = build_message(
                score=total_score,
                level=level,
                questions=QUESTIONS,
                scores=scores,
            )

            # まず診断ログ（memo空）を保存
            append_log_row(
                session_id=session_id,
                score=total_score,
                level=level,
                memo=""
            )

            logging.info("POST received")
            logging.info(f"session_id: {session_id}")
            logging.info(f"total_score: {total_score}")
            logging.info(f"level(internal): {level}")

            return render_template(
                "result.html",
                result={
                    "text": result_text,
                    "session_id": session_id,
                    "score": total_score,
                }
            )

        except Exception as e:
            logging.exception("POST /form failed")
            raise

    return render_template("form.html", questions=QUESTIONS)

@app.route("/memo", methods=["POST"])
def memo():
    try:
        session_id = request.form.get("session_id", "")
        score = int(request.form.get("score", "0"))
        memo_text = (request.form.get("memo") or "").strip()

        # 空メモは保存しない（任意）
        if memo_text:
            # memoログを追記（同じsession_idで紐づけ）
            level = get_level(score)
            append_log_row(
                session_id=session_id,
                score=score,
                level=level,
                memo=memo_text
            )

        return render_template("thanks.html")

    except Exception:
        logging.exception("POST /memo failed")
        raise

if __name__ == "__main__":
    app.run(debug=True)
