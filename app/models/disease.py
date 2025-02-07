from typing import List
from uuid import uuid4

from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship

from db.base_class import Base


class Disease(Base):
    __tablename__ = "disease"
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid4)

    name = Column(String, nullable=False)
    eppo_code = Column(String, nullable=False)
    base_gdd = Column(Integer, nullable=False)
    description = Column(String, nullable=True)

    gdd_points: Mapped[List["GDDInterval"]] = relationship(back_populates="disease", cascade="all, delete-orphan")
