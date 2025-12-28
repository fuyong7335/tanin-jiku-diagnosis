# app.py
import os
from uuid import uuid4

from flask import Flask, render_template, request
from diagnosis.logic import build_message, get_level
from services.sheets import append_result_row, append_memo_row


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")  # Renderでは環境変数推奨

# ====== 質問（あなたの10問に差し替えOK） ======
QUESTIONS = [
    {"id": 1, "text": "断る前に、相手の反応を先に想像してしまう", "choices": [
        ("当てはまらない", 0), ("あまり当てはまらない", 1), ("どちらでもない", 2), ("わりと当てはまる", 3), ("とても当てはまる", 4)
    ]},
    {"id": 2, "text": "自分で決めたはずなのに、誰かの許可が欲しくなることがある", "choices": [
        ("当てはまらない", 0), ("あまり当てはまらない", 1), ("どちらでもない", 2), ("わりと当てはまる", 3), ("とても当てはまる", 4)
    ]},
    {"id": 3, "text": "相手の機嫌が少し変わると、内容より先に心が動く", "choices": [
        ("当てはまらない", 0), ("あまり当てはまらない", 1), ("どちらでもない", 2), ("わりと当てはまる", 3), ("とても当てはまる", 4)
    ]},
    {"id": 4, "text": "本音を言う前に、正解っぽい言い方を探してしまう", "choices": [
        ("当てはまらない", 0), ("あまり当てはまらない", 1), ("どちらでもない", 2), ("わりと当てはまる", 3), ("とても当てはまる", 4)
    ]},
    {"id": 5, "text": "迷ったとき、自分の感覚より「波風が立たない方」を選びやすい", "choices": [
        ("当てはまらない", 0), ("あまり当てはまらない", 1), ("どちらでもない", 2), ("わりと当てはまる", 3), ("とても当てはまる", 4)
    ]},
    {"id": 6, "text": "「ちゃんとしなきゃ」が動機になっていることがある", "choices": [
        ("当てはまらない", 0), ("あまり当てはまらない", 1), ("どちらでもない", 2), ("わりと当てはまる", 3), ("とても当てはまる", 4)
    ]},
    {"id": 7, "text": "頑張っているのに、満たされなさが残ることがある", "choices": [
        ("当てはまらない", 0), ("あまり当てはまらない", 1), ("どちらでもない", 2), ("わりと当てはまる", 3), ("とても当てはまる", 4)
    ]},
    {"id": 8, "text": "選んだあとに「これでよかったのか」を繰り返し考えてしまう", "choices": [
        ("当てはまらない", 0), ("あまり当てはまらない", 1), ("どちらでもない", 2), ("わりと当てはまる", 3), ("とても当てはまる", 4)
    ]},
    {"id": 9, "text": "変わりたい気持ちはあるが、安全な場所を離れたくない", "choices": [
        ("当てはまらない", 0), ("あまり当てはまらない", 1), ("どちらでもない", 2), ("わりと当てはまる", 3), ("とても当てはまる", 4)
    ]},
    {"id": 10, "text": "人の期待を感じると、自分の気持ちより先に応えようとしてしまう", "choices": [
        ("当てはまらない", 0), ("あまり当てはまらない", 1), ("どちらでもない", 2), ("わりと当てはまる", 3), ("とても当てはまる", 4)
    ]},
]

# 結果をメモ投稿後に再描画するための一時キャッシュ（Render 1インスタンス想定）
RESULTS_CACHE = {}


@app.get("/")
def index():
    return render_template("form.html", questions=QUESTIONS)


@app.get("/form")
def form_get():
    return render_template("form.html", questions=QUESTIONS)


@app.post("/form")
def form_post():
    answers = []
    for q in QUESTIONS:
        v = int(request.form.get(f"answer{q['id']}", "0"))
        answers.append((q, v))

    total_score = sum(v for _, v in answers)

    # “高め”の項目を最大3つだけ AIに渡す（>=3 はおすすめ）
    highlights = [q["text"] for (q, v) in answers if v >= 3][:3]

    result = build_message(total_score, highlights=highlights)

    session_id = str(uuid4())
    RESULTS_CACHE[session_id] = {"result": result, "score": total_score}

    # スプシ保存（未設定でも落とさない設計）
    level = get_level(total_score)
    compact_answers = [(q["id"], v) for (q, v) in answers]
    append_result_row(
        score=total_score,
        level=level,
        ai_text=result["text"],
        highlights=highlights,
        answers=compact_answers,
    )

    return render_template(
        "result.html",
        result=result,
        session_id=session_id,
        score=total_score,
        memo_saved=False,
    )


@app.post("/memo")
def memo_post():
    memo = (request.form.get("memo") or "").strip()
    session_id = request.form.get("session_id") or ""
    score = int(request.form.get("score") or "0")

    if memo:
        append_memo_row(score=score, memo=memo)

    cached = RESULTS_CACHE.get(session_id)
    if not cached:
        # キャッシュが消えていても落とさない（最低限のサンクス）
        return "受け取りました。ありがとうございます。"

    return render_template(
        "result.html",
        result=cached["result"],
        session_id=session_id,
        score=cached["score"],
        memo_saved=True,
    )


if __name__ == "__main__":
    app.run(debug=True)
