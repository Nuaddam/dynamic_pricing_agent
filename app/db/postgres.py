import asyncpg
from app.core.config import settings


async def get_connection():
    return await asyncpg.connect(settings.POSTGRES_URL)