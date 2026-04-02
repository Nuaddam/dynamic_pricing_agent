from langchain_google_vertexai import ChatVertexAI
from app.core.config import settings

def get_llm():
    return ChatVertexAI(
        model="gemini-2.5-flash",
        project=settings.GOOGLE_PROJECT,
        location=settings.GOOGLE_LOCATION,
        temperature=0.2
    )