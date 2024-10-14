from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from db.base_class import Base


class Operator(Base):
    __tablename__ = "operator"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    symbol = Column(String)

    condition: Mapped["Condition"] = relationship(back_populates="operator")
