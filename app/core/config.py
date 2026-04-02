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

settings = Settings()