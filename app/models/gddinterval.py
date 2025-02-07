from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_class import Base


class GDDInterval(Base):
    __tablename__ = "gddinterval"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)

    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)
    descriptor = Column(String, nullable=False)

    disease_id: Mapped[int] = mapped_column(ForeignKey("disease.id"))
    disease: Mapped["Disease"] = relationship(back_populates="gdd_points")
