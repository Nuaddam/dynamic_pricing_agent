import hashlib
import json
import random
import time
from datetime import datetime, timedelta
from datetime import time as datetime_time
from functools import wraps

from pydantic import BaseModel

from app.db.postgres import db  # Import our stateful database pool object


def get_seconds_until_next_midnight() -> int:
    """Calculates exact remaining seconds until 00:00:00 of the next calendar day."""
    now = datetime.now()
    next_midnight = datetime.combine(now.date() + timedelta(days=1), datetime_time.min)
    return int((next_midnight - now).total_seconds())

def pg_midnight_cache():
    """Custom decorator to cache FastAPI endpoints inside PostgreSQL until midnight."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if db.pool is None:
                raise RuntimeError("Database connection pool has not been initialized.")

            # Find the primary Pydantic request model inside arguments dynamically
            req = next((arg for arg in args if isinstance(arg, BaseModel)), None)
            if not req and kwargs:
                req = next((val for val in kwargs.values() if isinstance(val, BaseModel)), None)

            if not req:
                raise TypeError("pg_midnight_cache requires a Pydantic model as a function argument.")

            # 1. Standardize the key by sorting dictionary keys before hashing
            payload_str = json.dumps(req.model_dump(), sort_keys=True)
            cache_key = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
            current_time = time.time()

            # 2. READ: Fetch data only if it is completely valid and unexpired
            async with db.pool.acquire() as conn:
                cached_value = await conn.fetchval(
                    "SELECT cache_value FROM function_cache WHERE cache_key = $1 AND expires_at > $2",
                    cache_key, current_time
                )
                if cached_value:
                    print("Cache hit for key:", cache_key)
                    return json.loads(cached_value)
            print("Cache miss for key:", cache_key)
            # 3. CACHE MISS: Execute the original function logic pipeline
            fresh_result = await func(*args, **kwargs)

            # 4. TTL calculations & payload string parsing
            ttl_seconds = get_seconds_until_next_midnight()
            expires_at_timestamp = current_time + ttl_seconds

            if hasattr(fresh_result, "model_dump"):
                serialized_value = json.dumps(fresh_result.model_dump())
            else:
                serialized_value = json.dumps(fresh_result)

            # 5. WRITE & LAZY CLEANUP: Save fresh record and clean out dead text blobs
            async with db.pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO function_cache (cache_key, cache_value, expires_at)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (cache_key) 
                    DO UPDATE SET cache_value = EXCLUDED.cache_value, expires_at = EXCLUDED.expires_at
                    """,
                    cache_key, serialized_value, expires_at_timestamp
                )
                
                # Periodically clean out old data safely while Cloud Run is processing active requests
                if random.random() < 0.1:
                    await conn.execute("DELETE FROM function_cache WHERE expires_at < $1", current_time)

            return fresh_result
        return wrapper
    return decorator