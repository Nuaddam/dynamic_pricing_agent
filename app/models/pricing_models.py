
from pydantic import BaseModel, Field


class PriceRequest(BaseModel):
    product_id: str
    product_name: str
    campaign_code: str
    model_name: str = Field(default="gemini-2.5-flash", description="The name of the LLM model to use for price adjustment")
    campaign_matrix: dict | None = Field(default_factory=dict, description="Optional campaign matrix for more complex campaign rules")


class PriceResponse(BaseModel):
    base_price: float
    campaign_price: float
    final_price: float
    sentiment: str
    confidence: float
    reasoning: str