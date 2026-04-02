from fastapi import APIRouter
from app.models.pricing_models import PriceRequest, PriceResponse
from app.services.pricing import calculate_price

router = APIRouter()


@router.post("/price", response_model=PriceResponse)
async def get_price(req: PriceRequest):
    result = await calculate_price(req.product_name, req.campaign_code)
    return result