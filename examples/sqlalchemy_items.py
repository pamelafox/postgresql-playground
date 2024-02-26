import os

from dotenv import load_dotenv
from pgvector.sqlalchemy import Vector
from sqlalchemy import Index, create_engine, func, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


# Define the models
class Base(DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    embedding = mapped_column(Vector(3))


# Connect to the database based on environment variables
load_dotenv(".env", override=True)
DBUSER = os.environ["DBUSER"]
DBPASS = os.environ["DBPASS"]
DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]
DATABASE_URI = f"postgresql://{DBUSER}:{DBPASS}@{DBHOST}/{DBNAME}"
# Use SSL if not connecting to localhost
if DBHOST != "localhost":
    DATABASE_URI += "?sslmode=require"
engine = create_engine(DATABASE_URI, echo=False)

# Create tables in database
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Insert data and issue queries
with Session(engine) as session:
    session.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

    index = Index(
        "my_index",
        Item.embedding,
        postgresql_using="hnsw",
        postgresql_with={"m": 16, "ef_construction": 64},
        postgresql_ops={"embedding": "vector_l2_ops"},
    )
    index.create(engine)

    session.add_all(
        [
            Item(embedding=[1, 2, 3]),
            Item(embedding=[-1, 1, 3]),
            Item(embedding=[0, -1, -2]),
        ]
    )

    # Find 2 closest vectors to [3, 1, 2]
    closest_items = session.scalars(select(Item).order_by(Item.embedding.l2_distance([3, 1, 2])).limit(2))
    for item in closest_items:
        print(item.embedding)

    # Calculate distance between [3, 1, 2] and the first vector
    distance = session.scalars(select(Item.embedding.l2_distance([3, 1, 2]))).first()
    print(distance)

    # Find vectors within distance 5 from [3, 1, 2]
    close_enough_items = session.scalars(select(Item).filter(Item.embedding.l2_distance([3, 1, 2]) < 5))
    for item in close_enough_items:
        print(item.embedding)

    # Calculate average of all vectors
    avg_embedding = session.scalars(select(func.avg(Item.embedding))).first()
    print(avg_embedding)
