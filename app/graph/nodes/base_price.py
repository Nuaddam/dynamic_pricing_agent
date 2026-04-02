import statistics


async def compute_base_price(state):
    prices = state["prices"]

    price_values = [p["price"] for p in prices]

    base_price = statistics.median(price_values)

    return {"base_price": base_price}