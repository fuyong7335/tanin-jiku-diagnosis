# logic.py
"""
他人軸（周りの反応に引っぱられやすい傾向）チェック用：結果文ロジック

方針：
- 画面に「傾向：」「問い：」「タイプ：」などのラベルは出さない
- さらっと話しかける口調（少し厳しめ、ただし人格否定はしない）
- “どの設問からそう言えるか”が伝わるように、強く出た設問の文言を自然に織り交ぜる
- AI連携は「差し込み（2〜4行＋質問1行＋次の一手1行）」だけに限定し、骨格は固定でブレない

使い方（例）：
    from logic import build_result

    answers = [0,1,2,0,1,2,1,2,1,3]  # 0..3（10問）
    result = build_result(answers)   # dict
    # result["lines"] を上から順に表示
"""

from __future__ import annotations

import os
import json
import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union


# =========================
# 設問（表示にも文生成にも使う）
# =========================

QUESTIONS: List[str] = [
    "人からどう思われるかを、つい気にしてしまう。",
    "何かを決めるとき、自分の気持ちより相手の気持ちを優先しがちだ。",
    "頼まれると断れないことが多い。",
    "モヤモヤや違和感を感じても、「気のせいかな」と無視することがある。",
    "誰かに迷惑をかけることが怖い。",
    "「ちゃんとしなきゃ」「がんばらなきゃ」と思いすぎて疲れる。",
    "本当はどうしたいのか、自分の気持ちが分からなくなる時がある。",
    "人から嫌われたくない気持ちが強い。",
    "相手に合わせすぎて、自分の意見を言えないことがある。",
    "感情が揺れたときに、「これって私が悪いのかな」と思いやすい。",
]


# =========================
# 回答 → 数値 変換（フォームが文字列を返す場合に対応）
# =========================

CHOICE_TO_SCORE: Dict[str, int] = {
    "あてはまらない": 0,
    "あまりない": 0,

    "少しあてはまる": 1,

    "あてはまる": 2,
    "わりとあてはまる": 2,

    "とてもあてはまる": 3,
}

# 10問・0..3想定の合計は 0..30
DEFAULT_THRESHOLDS = {
    "strong": 22,  # 22以上：強め
    "middle": 14,  # 14以上：ふつう〜やや強め
}


# =========================
# UI固定文（ラベル無しで表示できる形）
# =========================

HEAD_LINES = {
    "light":  "あなたの現在地は、周りを見ながらも自分に戻ってこられる場面が多そうです。",
    "middle": "あなたの現在地は、判断のハンドルが「自分の気持ち」より「周りの反応」に寄りやすいところがあるかもしれません。",
    "strong": "あなたの現在地は、相手の反応が判断を決めてしまいやすい時期かもしれません。",
}

HARD_LINES = {
    "light":  "ただ、疲れている日は反射で相手優先になりがちです。ここを曖昧にすると、じわっと消耗します。",
    "middle": "ここを曖昧にすると、また同じところで苦しくなります。だから少しだけ核心に触れます。",
    "strong": "ここを曖昧にすると、しんどさが積み上がります。だから少しだけ厳しく聞きます。",
}

CLOSING_LINE = "答えが出なくてもOKです。“引っかかった”なら、そこが入口です。"

INPUT_GUIDE = "よければ、引っかかった一文だけ残してください。短くてOKです。"
NOTICE = "※いただいた内容は今後のアプリ改善と傾向分析の参考として保存します。返信は行いません（送信完了メッセージのみ表示されます）。"
PLACEHOLDER = "例：引っかかった言葉／思い当たった場面／いま残っている感覚"
BUTTON_LABEL = "送信する"


# =========================
# 1問ごとの「血の通った」言い換え＆質問＆次の一手（固定版）
# =========================

QUESTION_RULES: Dict[int, Dict[str, List[str]]] = {
    0: {  # 人の目
        "lines": [
            "「どう思われるか」が先に立つ瞬間がありそうです。気づくと、自分の気持ちが後ろに下がる。",
            "頭の中で“正しい見せ方”を探すほど、本音が置き去りになりやすいです。",
        ],
        "questions": [
            "いちばん怖いのは「嫌われること」そのものですか？それとも「嫌われた時に自分がどう感じるか」ですか？",
            "その場で守ろうとしているものは何ですか？（評価／関係／空気 など）",
        ],
        "next_steps": [
            "よければ一度だけ、「私は今、好かれたい？正直でいたい？」を分けてみてください。",
        ],
    },
    1: {  # 相手優先
        "lines": [
            "決めるときに、相手の気持ちが先に完成してしまうことがありそうです。その分、自分の都合が遅れて出てくる。",
            "優しさが強みでも、続くと「自分が何を望んでいたか」がぼやけやすいです。",
        ],
        "questions": [
            "相手を優先したあと、あなたの中でいちばん残るのは何ですか？（疲れ／モヤモヤ／罪悪感 など）",
            "本当は、どんな順番で決められたら楽でしょう？",
        ],
        "next_steps": [
            "よければ次回だけ、結論の前に「私は今どうしたい？」を10秒だけ挟んでみてください。",
        ],
    },
    2: {  # 断れない
        "lines": [
            "断る前に相手の都合を優先して、気づいたら自分が後回し…になりやすいかもしれません。",
            "引き受けた瞬間はホッとする。でもあとから静かに苦しくなる。そんな流れが出やすいです。",
        ],
        "questions": [
            "断れなかった時、あなたは何を失っていますか？（時間／体力／集中／気分 など）",
            "断るとしたら、いちばん引っかかるのは何ですか？（罪悪感／相手の反応／関係の変化 など）",
        ],
        "next_steps": [
            "よければ次回だけ、「即答しない（保留）」を選んでみてください。断るより難易度が低い一手です。",
        ],
    },
    3: {  # 違和感スルー
        "lines": [
            "違和感を感じても「気のせい」で流せる強さがある反面、感覚のサインが届きにくくなることがあります。",
            "その場を回すために、自分の感覚を一時停止していませんか。",
        ],
        "questions": [
            "最近の違和感は、どの場面で出ましたか？（人／場所／言葉）",
            "違和感を無視したあと、体に出るサインはありますか？（疲れ／胃／眠気 など）",
        ],
        "next_steps": [
            "よければ今日だけ、違和感が出たら「今の気持ち：一語」だけメモしてみてください。",
        ],
    },
    4: {  # 迷惑恐怖
        "lines": [
            "「迷惑をかけたくない」が強いほど、必要以上に自分を小さくしてしまいやすいです。",
            "先に自分を責めることで、場を収めようとしていませんか。",
        ],
        "questions": [
            "それは“あなたの責任”ですか？それとも“あなたの役割”ですか？",
            "自分が悪いと感じた時、根拠は何ですか？（事実／想像／過去の癖）",
        ],
        "next_steps": [
            "よければ次回だけ、結論の前に「事実」と「想像」を分けてみてください。",
        ],
    },
    5: {  # ちゃんとしなきゃ
        "lines": [
            "「ちゃんとしなきゃ」が強いと、終わりがなくなります。真面目さが強みでも、燃料切れも起きやすいです。",
            "頑張るほど、休むことに罪悪感が出ていませんか。",
        ],
        "questions": [
            "“ちゃんと”って、誰の基準ですか？自分の基準ですか？",
            "今のあなたに必要なのは努力ですか？それとも回復ですか？",
        ],
        "next_steps": [
            "よければ今日だけ、「70点でOK」を一箇所だけ導入してみてください。",
        ],
    },
    6: {  # 自分が分からない
        "lines": [
            "自分の気持ちが分からなくなるのは、感覚が弱いからではなく、後回しにし続けた結果で起きることがあります。",
            "本音を出す前に“正しさ”や“配慮”が先に出ていませんか。",
        ],
        "questions": [
            "「本当はどうしたい？」が難しい時、「本当は何が嫌だった？」なら答えられますか？",
            "迷った時、あなたが一番避けたいのは何ですか？",
        ],
        "next_steps": [
            "よければ次回だけ、「やりたい／やりたくない」だけで選択肢を切ってみてください。",
        ],
    },
    7: {  # 嫌われたくない
        "lines": [
            "嫌われたくない気持ちが強いほど、判断が“相手基準”になりやすいです。優しさが、自分への圧に変わることがあります。",
            "空気を守れる人ほど、自分の気持ちを後回しにしてしまいます。",
        ],
        "questions": [
            "「嫌われたくない」が出た瞬間、頭の中で何が起きていますか？（想像している反応／最悪の結末 など）",
            "その関係を守るために、あなたは何を差し出していますか？",
        ],
        "next_steps": [
            "よければ一度だけ、「嫌われないための選択」か「後悔しないための選択」かを分けてみてください。",
        ],
    },
    8: {  # 意見が言えない
        "lines": [
            "合わせる力が強いぶん、自分の意見が“あとから出てくる”ことがありそうです。",
            "言えないのは弱さではなく、関係を壊さない工夫でもあります。ただ、続くと自分が消えます。",
        ],
        "questions": [
            "言えなかった時、あなたは何を守りましたか？そして何を失いましたか？",
            "小さく言うなら、どんな一言なら出せそうですか？",
        ],
        "next_steps": [
            "よければ次回だけ、「私はこう思う」を短く一言だけ言ってみてください。理由は後でいいです。",
        ],
    },
    9: {  # 感情が揺れると自責
        "lines": [
            "感情が揺れた時に「私が悪いのかな」に寄りやすいのは、責任感が強いサインでもあります。",
            "ただ、その癖が続くと、必要以上に自分を追い込みます。",
        ],
        "questions": [
            "それが“あなたのせい”だと言える根拠は、事実としてありますか？",
            "もし友達が同じ状況なら、あなたはその人に何と言いますか？",
        ],
        "next_steps": [
            "よければ次回だけ、感情が揺れたら「判断はあとで」を合言葉にしてみてください。",
        ],
    },
}


# =========================
# データ構造
# =========================

@dataclass
class Highlight:
    index: int          # 0..9
    value: int          # 0..3
    text: str           # 設問文


# =========================
# 基本ユーティリティ
# =========================

def normalize_answers(answers: Sequence[Union[int, str]]) -> List[int]:
    """
    answers: 数値（0..3）または選択肢文字列の配列
    """
    out: List[int] = []
    for a in answers:
        if isinstance(a, int):
            out.append(max(0, min(3, a)))
        else:
            s = str(a).strip()
            if s in CHOICE_TO_SCORE:
                out.append(CHOICE_TO_SCORE[s])
            else:
                # 想定外は0扱い（落ちないため）
                out.append(0)
    return out


def calc_total_score(answers: Sequence[int]) -> int:
    return int(sum(answers))


def get_level(total_score: int, thresholds: Optional[Dict[str, int]] = None) -> str:
    th = thresholds or DEFAULT_THRESHOLDS
    if total_score >= th["strong"]:
        return "strong"
    if total_score >= th["middle"]:
        return "middle"
    return "light"


def get_highlights(answers: Sequence[int], top_k: int = 2) -> List[Highlight]:
    """
    回答値が高い設問から top_k を抽出（2以上を優先）。
    """
    ranked = sorted(list(enumerate(answers)), key=lambda x: x[1], reverse=True)
    picks = [i for i, v in ranked if v >= 2][:top_k]
    # 2以上が無い場合は上位1つだけ拾う（根拠ゼロを避ける）
    if not picks and ranked:
        picks = [ranked[0][0]]

    res: List[Highlight] = []
    for i in picks:
        res.append(Highlight(index=i, value=int(answers[i]), text=QUESTIONS[i]))
    return res


# =========================
# AI連携（任意）
# =========================

AI_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "lines": {"type": "array", "minItems": 2, "maxItems": 4, "items": {"type": "string"}},
        "question": {"type": "string"},
        "next_step": {"type": "string"},
    },
    "required": ["lines", "question", "next_step"],
}

AI_SYSTEM_PROMPT = """
あなたは日本語の自己理解アプリの結果文ライターです。
トーン：少し厳しめ、でも受け取りやすい。人格否定は禁止。断定しない（「かもしれません」「〜しやすい」）。
禁止：見出しラベル（例「傾向：」「問い：」「診断結果：」「タイプ：」）を出さない。
禁止：レポート言葉（「今回の回答では」等）を使わない。
記号：箇条書き（・、-、1. 等）は避ける。文章として自然に。
出力：JSONスキーマに厳密準拠。画面にそのまま表示できる文章にする。
"""

def _can_use_ai(use_ai: Optional[bool]) -> bool:
    if use_ai is False:
        return False
    if use_ai is True:
        return bool(os.environ.get("OPENAI_API_KEY"))
    # None の場合：環境変数 USE_AI=1 かつ APIキーあり のときだけ有効
    return (os.environ.get("USE_AI") == "1") and bool(os.environ.get("OPENAI_API_KEY"))


def generate_ai_parts(level: str, total_score: int, highlights: List[Highlight]) -> Optional[Dict[str, str]]:
    """
    OpenAI SDK が入っていて、OPENAI_API_KEY がある場合のみAI生成。
    失敗したら None を返して固定文にフォールバック。
    """
    try:
        from openai import OpenAI  # type: ignore
    except Exception:
        return None

    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        payload = {
            "level": level,
            "total_score": total_score,
            "highlights": [
                {"text": h.text, "value": h.value}
                for h in highlights
            ],
        }

        resp = client.responses.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            input=[
                {"role": "system", "content": AI_SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ],
            max_output_tokens=260,
            temperature=0.7,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "result_parts",
                    "strict": True,
                    "schema": AI_SCHEMA,
                }
            },
        )

        data = json.loads(resp.output_text)
        # 最低限の整形
        lines = [str(x).strip() for x in data.get("lines", []) if str(x).strip()]
        question = str(data.get("question", "")).strip()
        next_step = str(data.get("next_step", "")).strip()
        if len(lines) < 2 or not question or not next_step:
            return None
        return {"lines": lines, "question": question, "next_step": next_step}
    except Exception:
        return None


# =========================
# 固定文（非AI）生成：設問に紐づける
# =========================

def generate_fixed_parts(level: str, highlights: List[Highlight]) -> Dict[str, Any]:
    """
    AIを使わない場合でも、強く出た設問（ハイライト）に紐づく文章を返す。
    """
    rng = random.Random()

    # 最重要：ハイライトの先頭を主軸にする
    primary = highlights[0]
    primary_rule = QUESTION_RULES.get(primary.index)

    # 保険
    if not primary_rule:
        primary_rule = {
            "lines": ["少しだけ核心に触れます。いまのあなたは、周りの反応が判断に混ざりやすいところがあるかもしれません。"],
            "questions": ["最近、「本当はこうしたかった」を飲み込んだ場面はありませんでしたか？"],
            "next_steps": ["よければ今日だけ、「自分の気持ち」を10秒確認してみてください。"],
        }

    lines: List[str] = []

    # “どの設問から？”を自然に織り交ぜる（Q番号は出さず、設問文をそのまま引用）
    lines.append(f"特に「{primary.text}」が強めに出ています。")

    # 設問ごとの“血の通った”言い換えを1行追加
    lines.append(rng.choice(primary_rule["lines"]))

    # 2つ目のハイライトがあるなら、補助で1行だけ足す（長くしすぎない）
    if len(highlights) >= 2:
        secondary = highlights[1]
        sec_rule = QUESTION_RULES.get(secondary.index)
        if sec_rule:
            # 2つ目は「補足」っぽく短く
            lines.append(f"もう一つ、「{secondary.text}」も気配として出ています。")

    question = rng.choice(primary_rule["questions"])
    next_step = rng.choice(primary_rule["next_steps"])

    # レベルに合わせて、少しだけ圧の調整（言い切りを避ける）
    if level == "light":
        # 軽めは質問を少し柔らかく
        if not question.endswith("？"):
            question += "？"
    elif level == "strong":
        # 強めは問いの切れ味を少し上げる（ただし人格否定はしない）
        question = question.replace("でしょうか", "ですか")

    return {"lines": lines, "question": question, "next_step": next_step}


# =========================
# 公開API：結果文を組み立てる
# =========================

def build_result(
    answers: Sequence[Union[int, str]],
    thresholds: Optional[Dict[str, int]] = None,
    use_ai: Optional[bool] = None,
    top_k_highlights: int = 2,
) -> Dict[str, Any]:
    """
    answers: 10問分（0..3 もしくは選択肢文字列）
    return:
        {
          "level": "light|middle|strong",
          "total_score": int,
          "lines": [表示用の文章（ラベル無し）],
          "input_guide": str,
          "notice": str,
          "placeholder": str,
          "button_label": str,
          "highlights": [{"index":int,"value":int,"text":str}, ...]  # UIに出さなくてOK（分析用）
        }
    """
    norm = normalize_answers(answers)
    total = calc_total_score(norm)
    level = get_level(total, thresholds=thresholds)
    highlights = get_highlights(norm, top_k=top_k_highlights)

    # AIパーツ（任意）
    parts: Optional[Dict[str, Any]] = None
    if _can_use_ai(use_ai):
        parts = generate_ai_parts(level=level, total_score=total, highlights=highlights)

    # フォールバック
    if not parts:
        parts = generate_fixed_parts(level=level, highlights=highlights)

    # 最終 lines（表示用）：固定骨格 +（AI or 固定差し込み）
    lines: List[str] = [
        HEAD_LINES[level],
        HARD_LINES[level],
        *parts["lines"],
        parts["question"],
        parts["next_step"],
        CLOSING_LINE,
    ]

    return {
        "level": level,
        "total_score": total,
        "lines": [x for x in (s.strip() for s in lines) if x],
        "input_guide": INPUT_GUIDE,
        "notice": NOTICE,
        "placeholder": PLACEHOLDER,
        "button_label": BUTTON_LABEL,
        "highlights": [
            {"index": h.index, "value": h.value, "text": h.text}
            for h in highlights
        ],
    }


# =========================
# 文字列としてまとめたい場合（任意）
# =========================

def join_lines(lines: Sequence[str], sep: str = "\n\n") -> str:
    """
    UIで段落として表示したい場合用
    """
    return sep.join([s for s in (str(x).strip() for x in lines) if s])
