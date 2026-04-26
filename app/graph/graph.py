from langgraph.graph import END, StateGraph

from app.graph.nodes.adjust import llm_adjust_price
from app.graph.nodes.base_price import compute_base_price
from app.graph.nodes.campaign import apply_campaign_rule
from app.graph.nodes.db import get_product_details, get_product_prices
from app.graph.nodes.pinecone import find_similar_products
from app.graph.nodes.search import get_market_data
from app.graph.nodes.sentiment import analyze_sentiment
from app.graph.state import PricingState

builder = StateGraph(PricingState)

builder.add_node("pinecone", find_similar_products)
builder.add_node("db_prices", get_product_prices)
builder.add_node("db_details", get_product_details)
builder.add_node("base", compute_base_price)
builder.add_node("search", get_market_data)
builder.add_node("sentiment", analyze_sentiment)
builder.add_node("campaign", apply_campaign_rule)
builder.add_node("adjust", llm_adjust_price)

builder.set_entry_point("pinecone")

builder.add_edge("pinecone", "db_prices")
builder.add_edge("db_prices", "db_details")
builder.add_edge("db_details", "base")
# builder.add_edge("base", END)
builder.add_edge("base", "search")
builder.add_edge("search", "sentiment")
builder.add_edge("sentiment", "campaign")
builder.add_edge("campaign", "adjust")

builder.add_edge("adjust", END)

graph = builder.compile()