import json
import os
from pathlib import Path

from dotenv import load_dotenv
from pgvector.sqlalchemy import Vector
from sqlalchemy import Index, create_engine, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


# Define the models
class Base(DeclarativeBase):
    pass


class Movie(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    title_vector = mapped_column(Vector(1536))  # ada-002 is 1536-dimensional


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
        "hnsw_index",
        Movie.title_vector,
        postgresql_using="hnsw",
        postgresql_with={"m": 16, "ef_construction": 64},
        postgresql_ops={"title_vector": "vector_cosine_ops"},
    )

    index.create(engine)

    # Insert the movies from the JSON file
    current_directory = Path(__file__).parent
    data_path = current_directory / "movies_ada002.json"
    with open(data_path) as f:
        movies = json.load(f)
        for title, title_vector in movies.items():
            movie = Movie(title=title, title_vector=title_vector)
            session.add(movie)
        session.commit()

    # Query the database
    query = select(Movie).where(Movie.title == "Winnie the Pooh")
    target_movie = session.execute(query).scalars().first()
    if target_movie is None:
        print("Movie not found")
        exit(1)

    # Find the 5 most similar movies to "Winnie the Pooh"
    closest = session.scalars(
        select(Movie).order_by(Movie.title_vector.cosine_distance(target_movie.title_vector)).limit(5)
    )
    for movie in closest:
        print(movie.title)
