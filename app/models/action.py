from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from db.base_class import Base


class Action(Base):
    __tablename__ = "action"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)
    description = Column(String)

    # rules: Mapped[List["Rule"]] = relationship(back_populates="action")
