from langchain_google_genai import GoogleGenerativeAI

from app.core.config import settings


def get_llm():
    return GoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.7
    )