import os
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

from dotenv import load_dotenv
from sqlalchemy import String, Column, Integer, Identity, select
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine

app = FastAPI()


# Pydantic model
class RestaurantIn(BaseModel):
    name: str
    address: Union[str, None] = None


# SqlAlchemy model
class Base(DeclarativeBase):
    pass


class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, Identity(start=1, cycle=True), primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(100), nullable=True)


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


@app.get("/")
def root():
    return "Welcome to the FastAPI and Postgres in a dev container demonstration. Add /docs to the URL to see API methods."


@app.get("/restaurant/{id}")
def get_restaurant(id: int):
    with Session(engine) as session:
        query = select(Restaurant).where(Restaurant.id == id)
        restaurants = session.execute(query).scalars().all()
        return f"{restaurants[0].id}, {restaurants[0].name}, {restaurants[0].address}"


@app.post("/restaurant")
def set_restaurant(item: RestaurantIn):
    with Session(engine) as session:
        restaurant = Restaurant(name=item.name, address=item.address)
        session.add(restaurant)
        session.commit()
        return f"Added restaurant with id {restaurant.id}."


@app.get("/all")
def get_all_restaurants():
    rows = []
    with Session(engine) as session:
        resturants = session.query(Restaurant).all()
        for restaurant in resturants:
            rows.append(f"{restaurant.id}, {restaurant.name}, {restaurant.address}")
    return rows
