import os


from dotenv import load_dotenv
import psycopg2


# Connect to the database
load_dotenv(".env")
DBUSER = os.environ["DBUSER"]
DBPASS = os.environ["DBPASS"]
DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]

conn = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST)
cur = conn.cursor()
cur.execute("INSERT INTO restaurants (id, name) VALUES ('3', 'test')")
conn.commit()
cur.close()