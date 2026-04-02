from app.core.llm import get_llm
# from langchain_core.output_parsers import JsonOutputParser

from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser


class AdjustResponse(BaseModel):
    final_price: float
    confidence: float
    reasoning: str

async def llm_adjust_price(state):
    llm = get_llm()

    parser = PydanticOutputParser(pydantic_object=AdjustResponse)

    prompt = f"""
    campaign_price: {state["campaign_price"]}
    sentiment: {state["sentiment"]}

    Adjust price within:
    +10% max
    -15% max

    Return JSON:
    {{
      "final_price": float,
      "confidence": float,
      "reasoning": string
    }}
    """

    chain = llm | parser

    result = await chain.ainvoke(prompt)

    return result.model_dump()