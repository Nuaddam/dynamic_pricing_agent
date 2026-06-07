# init_db.py
import asyncio

from app.db.postgres import get_connection


async def initialize_database():
    print("Connecting to PostgreSQL to initialize structures...")
    conn = await get_connection()
    try:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS function_cache (
                cache_key VARCHAR(64) PRIMARY KEY,
                cache_value TEXT NOT NULL,
                expires_at DOUBLE PRECISION NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_cache_expires ON function_cache (expires_at);
        """)
        print("PostgreSQL table and indexes successfully verified.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(initialize_database())
