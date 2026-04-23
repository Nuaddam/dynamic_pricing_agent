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
    
async def fetch_product_info(id):
    conn = await get_connection()
    rows = await conn.fetch(
        "SELECT id, name, description FROM products WHERE id = $1",
        id
    )

    return {
        "id": str(rows[0]["id"]),
        "name": rows[0]["name"],
        "description": rows[0]["description"],
        "price": float(rows[0]["price"])
    } if rows else None