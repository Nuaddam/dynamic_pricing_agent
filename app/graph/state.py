from typing import TypedDict, List


class PricingState(TypedDict):
    product_name: str
    campaign: str

    similar_product_ids: List[str]
    prices: List[float]

    base_price: float

    market_data: str
    sentiment: str

    campaign_price: float

    final_price: float
    confidence: float
    reasoning: str