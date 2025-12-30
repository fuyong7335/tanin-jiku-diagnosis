# app.py
import logging
logging.basicConfig(level=logging.INFO)

from dotenv import load_dotenv
load_dotenv()  # ローカル用（RenderではEnvironmentが使われる）

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
            for key, val in request.form.items():
                if key.startswith("answer"):
                    scores.append(int(val))

            total_score = sum(scores)
            result = build_message(total_score)

            logging.info("POST /form received")
            logging.info("total_score=%s level=%s", total_score, result["level"])

            return render_template("result.html", result=result, total_score=total_score)

        except Exception:
            logging.exception("=== POST ERROR (/form) ===")
            raise

    return render_template("form.html", questions=QUESTIONS)


@app.route("/message", methods=["POST"])
def message():
    try:
        user_message = (request.form.get("message") or "").strip()
        level = (request.form.get("level") or "").strip()
        score = (request.form.get("score") or "").strip()

        logging.info("POST /message received level=%s score=%s len=%s", level, score, len(user_message))

        # 空送信は保存しない（押し間違い対策）
        if user_message:
            save_message(level=level, score=score, message=user_message)

        return render_template("thanks.html")

    except Exception:
        logging.exception("=== POST ERROR (/message) ===")
        raise


if __name__ == "__main__":
    app.run(debug=True)
