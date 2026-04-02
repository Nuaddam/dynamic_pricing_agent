from app.services.pinecone import search_similar_products
from app.services.product import get_products_by_ids
from app.services.search import get_market_news
from app.services.sentiment import analyze_sentiment
from app.core.pricing_strategy import apply_campaign

import statistics


async def calculate_price(product_name: str, campaign_code: str):

    # Search via pc
    results = search_similar_products(product_name)

    product_ids = [r["id"] for r in results]

    # Connect to pg
    products = await get_products_by_ids(product_ids)

    prices = [p["price"] for p in products if p["price"]]
    base_price = statistics.median(prices)

    # Groundign extrernal news
    news = get_market_news(product_name)

    # Sentiment
    sentiment_data = analyze_sentiment(news)
    sentiment = sentiment_data["sentiment"]

    # Campaign logic
    final_price = apply_campaign(base_price, campaign_code, sentiment)

    return {
        "base_price": base_price,
        "final_price": final_price,
        "sentiment": sentiment,
        "reasoning": sentiment_data["reason"]
    }