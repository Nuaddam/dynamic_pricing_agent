from app.services.search import search_market


def get_market_data(state):
    data = search_market(state["product_name"])
    return {"market_data": data}