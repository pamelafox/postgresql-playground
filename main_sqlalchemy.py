import os


from dotenv import load_dotenv
from sqlalchemy import String, Column, Integer, Identity, select
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine

# Define the models
class Base(DeclarativeBase):
    pass

class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, Identity(start=1, cycle=True), primary_key=True)
    name = Column(String(100), nullable=False)


# Connect to the database
load_dotenv(".env")
DBUSER = os.environ["DBUSER"]
DBPASS = os.environ["DBPASS"]
DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]
DATABASE_URI = f"postgresql://{DBUSER}:{DBPASS}@{DBHOST}/{DBNAME}"
if DBHOST != "localhost":
    DATABASE_URI += "?sslmode=require"

engine = create_engine(DATABASE_URI, echo=True)

# Create tables in database
Base.metadata.create_all(engine)

# Insert data and issue queries
with Session(engine) as session:
    # insert restaurant
    restaurant = Restaurant(name="Test restaurant")
    session.add(restaurant)
    session.commit()

    # select restaurant "Test restaurant"
    query = select(Restaurant).where(Restaurant.name == "Test restaurant")
    restaurants = session.execute(query).scalars().all()
    print(restaurants)
    pass
