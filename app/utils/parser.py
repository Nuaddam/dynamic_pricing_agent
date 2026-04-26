import re


def extract_prices(text: str):
    prices = re.findall(r"\d+\.?\d*", text)
    return [float(p) for p in prices]


def clean_outliers(prices):
    if not prices:
        return []

    prices.sort()
    n = len(prices)
    return prices[int(n*0.1):int(n*0.9)]