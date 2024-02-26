import asyncio
import os

import asyncpg
from dotenv import load_dotenv
from pgvector.asyncpg import register_vector


async def main():
    # Establish a connection to an existing database
    load_dotenv(".env", override=True)
    DBUSER = os.environ["DBUSER"]
    DBPASS = os.environ["DBPASS"]
    DBHOST = os.environ["DBHOST"]
    DBNAME = os.environ["DBNAME"]

    DATABASE_URI = f"postgresql://{DBUSER}:{DBPASS}@{DBHOST}/{DBNAME}"

    # Use SSL if not connecting to localhost
    if DBHOST != "localhost":
        DATABASE_URI += "?sslmode=require"
    conn = await asyncpg.connect(DATABASE_URI)

    await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
    await register_vector(conn)

    await conn.execute("DROP TABLE IF EXISTS items")
    await conn.execute("CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3))")
    await conn.execute("CREATE INDEX ON items USING hnsw (embedding vector_l2_ops)")

    await conn.execute("INSERT INTO items (embedding) VALUES ($1)", [1, 2, 3])
    await conn.execute("INSERT INTO items (embedding) VALUES ($1)", [-1, 1, 3])
    await conn.execute("INSERT INTO items (embedding) VALUES ($1)", [0, -1, -2])

    # Find 2 closest vectors to [3, 1, 2]
    row = await conn.fetch("SELECT * FROM items ORDER BY embedding <-> $1 LIMIT 2", [3, 1, 2])
    for row in row:
        print(row["embedding"])

    # Calculate distance between [3, 1, 2] and the first vector
    row = await conn.fetch(
        "SELECT embedding <-> $1 AS distance FROM items ORDER BY embedding <-> $1 LIMIT 1", [3, 1, 2]
    )
    print(row[0]["distance"])

    # Find vectors within distance 5 from [3, 1, 2]
    row = await conn.fetch("SELECT * FROM items WHERE embedding <-> $1 < 5", [3, 1, 2])
    for row in row:
        print(row["embedding"])

    # Calculate average of all vectors
    row = await conn.fetch("SELECT avg(embedding) FROM items")
    print(row[0]["avg"])

    # Close the connection.
    await conn.close()


asyncio.get_event_loop().run_until_complete(main())
