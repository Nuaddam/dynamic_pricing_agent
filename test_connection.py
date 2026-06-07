# test_connection.py
import asyncio

import asyncpg

# Your current credentials configuration
DB_USER = "postgres"
DB_PASSWORD = None  # Handled dynamically below
DB_NAME = "hyper_personalize_ads"
DB_HOST = "127.0.0.1"
DB_PORT = 5432

async def run_test():
    print("=== STARTING POSTGRESQL CONNECTION TEST ===")
    print(f"Target: {DB_HOST}:{DB_PORT} | Database: {DB_NAME} | User: {DB_USER}")
    
    # Strategy 1: Test with an explicit empty string ""
    print("\n[Strategy 1] Attempting connection with an empty string password...")
    try:
        conn = await asyncpg.connect(
            user=DB_USER,
            password="",  # Empty string fallback
            database=DB_NAME,
            host=DB_HOST,
            port=DB_PORT,
            timeout=5  # Prevents hanging forever if the host is wrong
        )
        print("✅ SUCCESS! Connected successfully using Strategy 1.")
        
        # Test basic query execution
        version = await conn.fetchval("SELECT version();")
        print(f"Database version: {version}")
        
        await conn.close()
        return
    except Exception as e:
        print(f"❌ Strategy 1 Failed: {e}")

    # Strategy 2: Test by completely omitting the password field
    print("\n[Strategy 2] Attempting connection by omitting the password parameter...")
    try:
        conn = await asyncpg.connect(
            user=DB_USER,
            database=DB_NAME,
            host=DB_HOST,
            port=DB_PORT,
            timeout=5
        )
        print("✅ SUCCESS! Connected successfully using Strategy 2.")
        await conn.close()
        return
    except Exception as e:
        print(f"❌ Strategy 2 Failed: {e}")

    print("\n=== TEST CONCLUSION ===")
    print("Could not connect to PostgreSQL. Common causes:")
    print("1. Your local PostgreSQL server is not running.")
    print("2. The database 'hyper_personalize_ads' does not exist yet.")
    print("3. pg_hba.conf requires a password or trust authentication is misconfigured.")

if __name__ == "__main__":
    asyncio.run(run_test())
