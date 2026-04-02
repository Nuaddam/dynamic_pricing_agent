from pinecone import Pinecone
from app.core.config import settings

# init client
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# connect index
index = pc.Index("products",host=settings.PINECONE_INDEX_HOST)


def search_similar_products(product_text: str, top_k: int = 7):
    response = index.search(
        namespace="hyper-personalization-ads",
        query={
            "inputs": {"text": product_text},
            "top_k": top_k
        }
    )

    return [
        m["_id"]
        for m in response["result"]["hits"]
    ]