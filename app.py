# app.py
# tanin-jiku-diabnosis の起点ファイル
# 役割：アプリ起動・ルーティング・env読み込み

import logging
logging.basicConfig(level=logging.INFO)
from dotenv import load_dotenv
load_dotenv()  # ★ 必ず最初に読む（env方式の要）

from flask import Flask, render_template, request

from diagnosis.questions import QUESTIONS
from diagnosis.logic import build_message
from services.sheets import save_result

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        try:
            email = request.form.get("email")
            
            scores = []
            for key in request.form:
                if key.startswith("answer"):
                    scores.append(int(request.form[key]))

            total_score = sum(scores)
            result = build_message(total_score)

            # ログ出力（必ず Render Logs に出る）
            logging.info("POST received")
            logging.info(f"total_score: {total_score}")
            logging.info(f"result level: {result['level']}")
            logging.info(f"email: {email}")
            

            save_result(result["level"], total_score)

            return render_template("result.html", result=result)

        except Exception as e:
            print("=== POST ERROR ===")
            print(e)
            raise

    return render_template("form.html", questions=QUESTIONS)



if __name__ == "__main__":
    app.run(debug=True)
