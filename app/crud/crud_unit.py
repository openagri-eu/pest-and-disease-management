from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import Unit
from schemas import UnitCreate, UnitUpdate


class CrudUnit(CRUDBase[Unit, UnitCreate, UnitUpdate]):

    def get_all(self, db: Session):
        return db.query(Unit).all()

    def get_by_name(self, db: Session, name: str):
        return db.query(Unit).filter(Unit.name == name).first()

    def get_by_symbol(self, db: Session, symbol: str):
        return db.query(Unit).filter(Unit.symbol == symbol).first()


unit = CrudUnit(Unit)
