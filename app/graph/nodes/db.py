from app.services.product import fetch_prices


async def get_product_prices(state):
    prices = await fetch_prices(state["similar_product_ids"])
    return {"prices": prices}