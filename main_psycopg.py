import os

import psycopg2
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential

# Connect to the database
load_dotenv(".env", override=True)
DBUSER = os.environ["DBUSER"]
DBPASS = os.environ["DBPASS"]
azure_credential = DefaultAzureCredential()
#DBPASS = azure_credential.get_token("https://ossrdbms-aad.database.windows.net")
DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]

conn = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST)
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS restaurants")
cur.execute("CREATE TABLE restaurants (id SERIAL PRIMARY KEY,name VARCHAR(255) NOT NULL)")
cur.execute("INSERT INTO restaurants (id, name) VALUES ('3', 'test')")
conn.commit()
cur.close()
