import os


from dotenv import load_dotenv
from sqlalchemy import String
from sqlalchemy import select, func
from sqlalchemy.orm import Session, Mapped
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine


# Define the models
class Base(DeclarativeBase):
    pass


class Restaurant(Base):
    __tablename__ = "restaurants"
    id: Mapped[int] = mapped_column("id", String, primary_key=True)
    name: Mapped[str] = mapped_column("name", String)


# Connect to the database
load_dotenv(".env")
DBUSER = os.environ["DBUSER"]
DBPASS = os.environ["AZURE_POSTGRES_PASSWORD"]
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
    query = select(func.count(Restaurant.id))
    result = session.execute(query)
    print(result.scalar())
    # create restaurant
    restaurant = Restaurant(id="1", name="test")
    session.add(restaurant)
    session.commit()
