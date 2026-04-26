import json

from langchain_core.messages import HumanMessage, SystemMessage

from app.core.llm import get_llm

llm = get_llm()

def summarize_market(news_text: str):
    messages = [
        SystemMessage(content="""
    Extract market insight:
    - price_trend (up/down/stable)
    - demand (high/low)
    - sentiment (positive/negative)

    Return JSON only.
    """),
        HumanMessage(content=news_text)
    ]

    res = llm.invoke(messages)
    return json.loads(res.content)