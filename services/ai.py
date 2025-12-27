# services/ai.py
import os
from openai import OpenAI

# OpenAI公式SDKの基本形（client.responses.create / response.output_text）
# https://platform.openai.com/docs/guides/conversation-state 参照
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_text(prompt: str, model: str = "gpt-4o-mini") -> str:
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set")

    res = client.responses.create(
        model=model,
        input=prompt,
        max_output_tokens=220,
    )
    text = (res.output_text or "").strip()
    return text
