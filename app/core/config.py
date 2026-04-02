import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

    GOOGLE_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
    GOOGLE_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_HOST = os.getenv("PINECONE_INDEX_HOST")

    POSTGRES_URL = os.getenv("POSTGRES_URL")

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")

    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

settings = Settings()