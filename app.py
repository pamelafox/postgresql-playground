from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Using SQLAlchemy 2.0 with Declarative Base and Mapped classes


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[Optional[str]]
