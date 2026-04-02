from app.services.pinecone import search_similar_products

async def find_similar_products(state):
    ids = search_similar_products(state["product_name"])
    return {"similar_product_ids": ids}