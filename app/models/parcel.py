from typing import List

from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import Mapped, relationship

from db.base_class import Base


class Parcel(Base):
    __tablename__ = "parcel"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    data: Mapped[List["Data"]] = relationship(back_populates="parcel", cascade="all, delete-orphan")
