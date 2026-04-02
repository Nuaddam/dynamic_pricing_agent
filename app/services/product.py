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


async def fetch_prices(ids):
    conn = await get_connection()
    rows = await conn.fetch(
        "SELECT id, price FROM products WHERE id = ANY($1)",
        ids
    )

    return [
        {
            "id": str(r["id"]),
            "price": float(r["price"])  # 🔥 convert ตรงนี้
        }
        for r in rows
    ]