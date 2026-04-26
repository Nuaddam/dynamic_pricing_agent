from tavily import TavilyClient

from app.core.config import settings


def search_market(query: str):
    client = TavilyClient(api_key=settings.TAVILY_API_KEY)
    res = client.search(
        query=f"{query} price trend demand news ecommerce",
        search_depth="advanced",
        max_results=5
    )

    contents = []

    for r in res["results"]:
        contents.append(f"""TITLE: {r['title']}\nCONTENT: {r['content']}\nSCORE: {r['score']}""")

    return "\n\n".join(contents)