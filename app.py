# app.py
import logging
logging.basicConfig(level=logging.INFO)

from dotenv import load_dotenv
load_dotenv()  # ローカル用（Renderでは環境変数が入る）

from flask import Flask, render_template, request

from diagnosis.questions import QUESTIONS
from diagnosis.logic import build_message
from services.sheets import save_message

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        try:
            scores = []
            for key in request.form:
                if key.startswith("answer"):
                    scores.append(int(request.form[key]))

            total_score = sum(scores)
            result = build_message(total_score)

            logging.info("POST /form received")
            logging.info(f"total_score: {total_score}")
            logging.info(f"level: {result['level']}")

            return render_template(
                "result.html",
                result=result,
                total_score=total_score
            )

        except Exception:
            logging.exception("=== POST ERROR (/form) ===")
            raise

    return render_template("form.html", questions=QUESTIONS)


@app.route("/message", methods=["POST"])
def message():
    try:
        user_message = (request.form.get("message") or "").strip()
        level = request.form.get("level") or ""
        score = request.form.get("score") or ""

        logging.info("POST /message received")
        logging.info(f"level: {level}, score: {score}, message_len: {len(user_message)}")

        # 空送信は保存しない（押し間違い対策）
        if user_message:
            save_message(level=level, score=str(score), message=user_message)

        return render_template("thanks.html")

    except Exception:
        logging.exception("=== POST ERROR (/message) ===")
        raise


if __name__ == "__main__":
    app.run(debug=True)
