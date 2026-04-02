from langchain_core.output_parsers import StrOutputParser
from app.core.llm import get_llm

parser = StrOutputParser()

async def analyze_sentiment(state):
    prompt = f"""
    Classify sentiment:

    {state["market_data"]}

    Return: positive | neutral | negative
    """

    llm = get_llm()
    chain = llm | parser

    result = await chain.ainvoke(prompt)

    return {"sentiment": result.strip().lower()}