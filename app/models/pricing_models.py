from pydantic import BaseModel


class PriceRequest(BaseModel):
    product_name: str
    campaign_code: str


class PriceResponse(BaseModel):
    base_price: float
    campaign_price: float
    final_price: float
    sentiment: str
    confidence: float
    reasoning: str