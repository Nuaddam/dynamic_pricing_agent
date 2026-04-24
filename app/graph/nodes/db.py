from app.services.product import fetch_prices, fetch_product_info


async def get_product_prices(state):
    prices = await fetch_prices(state["similar_product_ids"])
    return {"prices": prices}

async def get_product_details(state):
    product_details = await fetch_product_info(state["product_id"])
    return {"product_details": product_details}