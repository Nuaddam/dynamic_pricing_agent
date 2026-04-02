from app.db.postgres import get_connection


async def get_products_by_ids(product_ids: list[str]):
    conn = await get_connection()

    query = """
    SELECT id, name, price
    FROM products
    WHERE id = ANY($1)
    """

    rows = await conn.fetch(query, product_ids)
    await conn.close()

    return [dict(r) for r in rows]