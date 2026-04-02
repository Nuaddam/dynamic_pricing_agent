from langchain_google_vertexai import ChatVertexAI
import json
from app.core.llm import get_llm

llm = get_llm()


def analyze_sentiment(text: str):
    prompt = f"""
    Analyze sentiment:

    {text}

    Return JSON:
    {{
        "sentiment": "positive | neutral | negative",
        "reason": "short"
    }}
    """

    res = llm.invoke(prompt)

    return json.loads(res.content)