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
    session.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

    index = Index(
        "my_index",
        Item.embedding,
        postgresql_using="hnsw",
        postgresql_with={"m": 16, "ef_construction": 64},
        postgresql_ops={"embedding": "vector_l2_ops"},
    )
    # or
    index = Index(
        "my_index",
        Item.embedding,
        postgresql_using="ivfflat",
        postgresql_with={"lists": 100},
        postgresql_ops={"embedding": "vector_l2_ops"},
    )

    index.create(engine)

    item = Item(embedding=[1, 2, 3])
    session.add(item)
    session.commit()

    closest = session.scalars(select(Item).order_by(Item.embedding.l2_distance([3, 1, 2])).limit(5))
    print(list(closest))

    distance = session.scalars(select(Item.embedding.l2_distance([3, 1, 2])))
    print(list(distance))

    close_enough = session.scalars(select(Item).filter(Item.embedding.l2_distance([3, 1, 2]) < 5))
    print(list(close_enough))

    session.scalars(select(func.avg(Item.embedding))).first()
