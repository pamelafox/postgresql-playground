import os

import numpy as np
import psycopg2
from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector

load_dotenv(".env", override=True)
DBUSER = os.environ["DBUSER"]
DBPASS = os.environ["DBPASS"]
DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]
# Use SSL if not connecting to localhost
DBSSL = "disable"
if DBHOST != "localhost":
    DBSSL = "require"

conn = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST, sslmode=DBSSL)
conn.autocommit = True
cur = conn.cursor()
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
cur.execute("DROP TABLE IF EXISTS items")
cur.execute("CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));")
register_vector(conn)

cur.execute("CREATE INDEX ON items USING hnsw (embedding vector_l2_ops)")

embeddings = [
    np.array([1, 2, 3]),
    np.array([-1, 1, 3]),
    np.array([0, -1, -2]),
]
for embedding in embeddings:
    cur.execute("INSERT INTO items (embedding) VALUES (%s)", (embedding,))

# Find 2 closest vectors to [3, 1, 2]
query_embedding = np.array([3, 1, 2])
cur.execute("SELECT * FROM items ORDER BY embedding <-> %s LIMIT 2", (query_embedding,))
closest_items = cur.fetchall()
for item in closest_items:
    print(item[1])

# Calculate distance between [3, 1, 2] and the first vector
cur.execute("SELECT embedding <-> %s AS distance FROM items ORDER BY embedding <-> %s LIMIT 1", (query_embedding, query_embedding))
distance = cur.fetchone()
print(distance[0])

# Find vectors within distance 5 from [3, 1, 2]
cur.execute("SELECT * FROM items WHERE embedding <-> %s < 5", (query_embedding,))
close_enough_items = cur.fetchall()
for item in close_enough_items:
    print(item[1])

# Calculate average of all vectors
cur.execute("SELECT avg(embedding) FROM items")
avg_embedding = cur.fetchone()
print(avg_embedding[0])

cur.close()
