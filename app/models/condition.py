from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.base_class import Base


class Condition(Base):
    __tablename__ = "condition"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)

    rule_id: Mapped[int] = mapped_column(ForeignKey("rule.id"))
    rule: Mapped["Rule"] = relationship(back_populates="conditions")

    unit_id: Mapped[int] = mapped_column(ForeignKey("unit.id"))
    unit: Mapped["Unit"] = relationship(back_populates="condition")

    operator_id: Mapped[int] = mapped_column(ForeignKey("operator.id"))
    operator: Mapped["Operator"] = relationship(back_populates="condition")

    value = Column(Float)
