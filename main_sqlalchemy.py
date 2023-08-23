import os

from dotenv import load_dotenv
from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


# Define the models
class Base(DeclarativeBase):
    pass


class Restaurant(Base):
    __tablename__ = "restaurants"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String, nullable=True)


# Connect to the database
load_dotenv(".env", override=True)
DBUSER = os.environ["DBUSER"]
DBPASS = os.environ["DBPASS"]
DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]
DATABASE_URI = f"postgresql://{DBUSER}:{DBPASS}@{DBHOST}/{DBNAME}"
if DBHOST != "localhost":
    DATABASE_URI += "?sslmode=require"
engine = create_engine(DATABASE_URI, echo=True)

# Create tables in database
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Insert data and issue queries
with Session(engine) as session:
    for i in range(10):
        session.add(Restaurant(name=f"Cheese Shop #{i}"))
    session.commit()

    query = select(Restaurant)
    results = session.execute(query)