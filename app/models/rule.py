from typing import List

from sqlalchemy import Column, Integer, String, TIME
from sqlalchemy.orm import Mapped, relationship

from db.base_class import Base


class Rule(Base):
    __tablename__ = "rule"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)

    name = Column(String)
    description = Column(String, nullable=True)
    from_time = Column(TIME, nullable=False)
    to_time = Column(TIME, nullable=False)

    conditions: Mapped[List["Condition"]] = relationship(back_populates="rule", cascade="all,delete")
