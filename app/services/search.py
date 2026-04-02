from langchain_google_community import GoogleSearchResults
from app.core.config import settings

search = GoogleSearchResults(api_key=settings.GOOGLE_API_KEY)


def get_market_news(product_name: str):
    query = f"{product_name} price trend news"

    return search.run(query)