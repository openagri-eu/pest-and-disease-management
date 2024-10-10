from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped

from db.base_class import Base


class Unit(Base):
    __tablename__ = "unit"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)
    symbol = Column(String)

    condition: Mapped["Condition"] = relationship(back_populates="unit")
