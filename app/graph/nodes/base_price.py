import statistics


def remove_outliers_iqr(data):
    """Calculates the median after removing outliers using only the statistics module."""
    if not data:
        return None

    # Sort data to ensure accurate quartile calculation
    sorted_data = sorted(data)

    # Calculate Q1 (25th percentile) and Q3 (75th percentile)
    # method='inclusive' matches standard statistical formulas
    q1, _, q3 = statistics.quantiles(sorted_data, n=4, method="inclusive")
    iqr = q3 - q1

    # Define outlier boundaries
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Filter out the outliers
    filtered_data = [x for x in sorted_data if lower_bound <= x <= upper_bound]
    return filtered_data

async def compute_base_price(state):
    prices = state["prices"]
    product = state["product_details"]

    price_values = [p["price"] for p in prices]

    filtered_prices = remove_outliers_iqr(price_values)
    base_price = statistics.median(filtered_prices) if filtered_prices else None
    if base_price is None and product and "price" in product:
        base_price = product["price"]
    if base_price is None:
        base_price = statistics.median(price_values)
        
    print(f"Computed base price: {base_price}, based on prices: {price_values} and product price: {product['price'] if product else 'N/A'}")
    print(f"Filtered prices (after removing outliers): {filtered_prices}")

    return {"base_price": base_price}