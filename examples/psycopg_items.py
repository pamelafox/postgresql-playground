import os

import psycopg2
from dotenv import load_dotenv

# Connect to the database
load_dotenv(".env", override=True)
DBUSER = os.environ["DBUSER"]
DBPASS = os.environ["DBPASS"]
DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]
# Use SSL if not connecting to localhost
sslmode = "disable"
if DBHOST != "localhost":
    sslmode = "require"
conn = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST, sslmode=sslmode)
cur = conn.cursor()
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
cur.execute("DROP TABLE IF EXISTS items")
cur.execute("CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));")
cur.execute("INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]');")
cur.execute("SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;")
conn.commit()
cur.close()
