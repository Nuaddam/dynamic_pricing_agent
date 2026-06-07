import asyncpg

from app.core.config import settings


async def get_connection():
    return await asyncpg.connect(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
    )
    
class Database:
    def __init__(self):
        self.pool: asyncpg.Pool | None = None

    async def initialize(self):
        """Initializes the global asyncpg connection pool."""
        self.pool = await asyncpg.create_pool(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            min_size=1,
            max_size=10  # Scaled for Google Cloud Run concurrency
        )
        print("PostgreSQL connection pool initialized.")

    async def close(self):
        """Safely closes the connection pool on application shutdown."""
        if self.pool:
            await self.pool.close()
        print("PostgreSQL connection pool closed.")

# Export a single stateful instance to use across your files
db = Database()