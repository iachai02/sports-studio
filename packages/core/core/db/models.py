from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, func
from typing import Optional
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())