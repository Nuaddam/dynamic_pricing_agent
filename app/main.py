from fastapi import FastAPI
from app.models.pricing_models import PriceRequest, PriceResponse
from app.graph.graph import graph

app = FastAPI()


@app.post("/price", response_model=PriceResponse)
async def price(req: PriceRequest):
    result = await graph.ainvoke({
        "product_name": req.product_name,
        "campaign": req.campaign_code
    })

    return result