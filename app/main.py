from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.cache import pg_midnight_cache
from app.db.postgres import db
from app.graph.graph import graph
from app.models.pricing_models import PriceRequest, PriceResponse


async def lifespan(app: FastAPI):
    # Instantly connects database engine on startup so Cloud Run passes health probes
    await db.initialize()
    yield
    # Closes pools cleanly when instance is scaled down
    await db.close()

app = FastAPI(lifespan=lifespan)


@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/price", response_model=PriceResponse)
@pg_midnight_cache()  # Decorator manages request inspection, DB transactions, and fallbacks
async def price(req: PriceRequest):
    start = datetime.now()
    result = await graph.ainvoke({
        "product_name": req.product_name,
        "campaign": req.campaign_code,
        "product_id": req.product_id,
        "model_name": req.model_name,
        "campaign_matrix": req.campaign_matrix
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