from google.genai import types
from pydantic import BaseModel

from app.utils.gemini import generate_content


class AdjustResponse(BaseModel):
    final_price: float
    confidence: float
    reasoning: str

SYSTEM_PROMPT = """
ROLE: You are an experienced Revenue Management Specialist. You have a background in dynamic pricing algorithms and consumer behavior analytics. Your personality is strategic and data-driven.

CONTEXT: You are working on a hyper-personalized ads app where product prices must be adjusted in real-time. You receive the current campaign price and the sentiment (positive, neutral, or negative) derived from market data to determine an optimal final price.

TASK: Calculate and adjust the product price based on the provided sentiment score while staying within strict percentage boundaries.

GOAL: The desired outcome is an optimized final price that maximizes conversion probability based on consumer sentiment.

CONSTRAINTS: 
    * The maximum price increase allowed is +10% of the original campaign_price.
    * The maximum price decrease allowed is -15% of the original campaign_price.
    * Use the sentiment to drive the direction: increase for 'positive', 'strongly positive', maintain for 'neutral', and decrease for 'negative', 'strongly negative'.
    * Ensure the output is a valid JSON object without markdown formatting.

FORMAT: Present your response as a JSON object with the following structure:
{
  "final_price": float,
  "confidence": float,
  "reasoning": string
}
"""

async def llm_adjust_price(state):
    product = state["product_details"]
    parts = [
		types.Part.from_text(text="Optimizes product pricing dynamically based on consumer sentiment and campaign performance data."),
		types.Part.from_text(text=f"PRODUCT NAME: {product['name']}\nDESCRIPTION: {product['description']}\nPRICE: {product['price']}"),
		types.Part.from_text(text=f"Current campaign price: {state['campaign_price']}\nMarket sentiment: {state['sentiment']}"),
	]
    response = generate_content(parts, system_instruction=SYSTEM_PROMPT, response_schema=AdjustResponse.model_json_schema())
    try:
        adjust_result = AdjustResponse.model_validate_json(response.text)
        return adjust_result.model_dump()
    except Exception as e:
        print(f"Error parsing LLM response: {e}")
    return {
		"final_price": state["campaign_price"],
		"confidence": 0.0,
		"reasoning": "Failed to parse LLM response, returning original campaign price."
	}