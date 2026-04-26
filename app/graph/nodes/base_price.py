import statistics


async def compute_base_price(state):
    prices = state["prices"]

    price_values = [p["price"] for p in prices]

    base_price = statistics.median(price_values)
    
    product = state["product_details"]
    base_price = product["price"] if product and "price" in product else base_price
    print(f"Computed base price: {base_price}, based on prices: {price_values} and product price: {product['price'] if product else 'N/A'}")

    return {"base_price": base_price}