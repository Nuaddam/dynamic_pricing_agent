# from pydantic import BaseModel, Field

# class PriceResponse(BaseModel):
#     new_price: float = Field(..., description="Final optimized price")
#     logic: str = Field(..., description="Explanation of pricing decision")

from pydantic import BaseModel


class PriceRequest(BaseModel):
    product_name: str
    campaign_code: str


class PriceResponse(BaseModel):
    base_price: float
    final_price: float
    sentiment: str
    reasoning: str