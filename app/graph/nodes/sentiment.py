from google.genai import types

from app.utils.gemini import generate_content

SYSTEM_PROMPT = """
ROLE: You are an experienced Marketing Data Scientist. You have a background in consumer sentiment analysis and market trend forecasting. Your personality is analytical, objective, and precise.

CONTEXT: You are working on a hyper-personalized ads application that dynamically matches products to consumers. You must evaluate how a specific product resonates with current market conditions based on name, description, price, and structured market data.

TASK: Analyze the sentiment of the provided product by correlating its features and price against the market data TITLE, CONTENT, and SCORE.

GOAL: The desired outcome is a single-label classification of the product's market standing.

CONSTRAINTS: 
    * Use only the following labels: strongly positive | positive | neutral | negative | strongly negative.
    * The price must be evaluated against the market data SCORE to determine if the product is perceived as high-value or poorly positioned.
    * Do not provide any justification or additional text; output only the label.
    * Ensure the sentiment is grounded strictly in the provided market data to prevent hallucinating consumer trends.
"""

async def analyze_sentiment(state):
    product = state["product_details"]
    parts = [
        types.Part.from_text(text="Analyzes product-market fit by correlating product descriptions and pricing with real-time market sentiment data."),
        types.Part.from_text(text=f"PRODUCT NAME: {product['name']}\nDESCRIPTION: {product['description']}\nPRICE: {product['price']}"),
        types.Part.from_text(text=state["market_data"]),
    ]
    response = generate_content(parts=parts, system_instruction=SYSTEM_PROMPT)

    return {"sentiment": response.text.strip().lower()}