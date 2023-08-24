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
cur.execute("DROP TABLE IF EXISTS restaurants")
cur.execute("CREATE TABLE restaurants (id SERIAL PRIMARY KEY,name VARCHAR(255) NOT NULL)")
cur.execute("INSERT INTO restaurants (id, name) VALUES ('3', 'test')")
conn.commit()
cur.close()
