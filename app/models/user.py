from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_class import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    email = Column(String,  index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
