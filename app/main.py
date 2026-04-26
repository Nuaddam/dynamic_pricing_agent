from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.graph.graph import graph
from app.models.pricing_models import PriceRequest, PriceResponse

app = FastAPI()

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/price", response_model=PriceResponse)
async def price(req: PriceRequest):
    start = datetime.now()
    result = await graph.ainvoke({
        "product_name": req.product_name,
        "campaign": req.campaign_code,
        "product_id": req.product_id,
    })
    end = datetime.now()
    print("Total processing time:", (end - start).total_seconds(), "seconds")

    return result

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              # List of allowed origins
    allow_credentials=True,           # Allow cookies/authentication headers
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allow all headers
)