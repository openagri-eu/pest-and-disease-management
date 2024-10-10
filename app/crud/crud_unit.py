from typing import Optional

from sqlalchemy.orm import Session

from core.security import verify_password, get_password_hash
from crud.base import CRUDBase
from models import Unit
from schemas import UnitCreate, UnitUpdate


class CrudUnit(CRUDBase[Unit, UnitCreate, UnitUpdate]):

    def get_all(self, db: Session):
        return db.query(Unit).all()

    def get_by_name(self, db: Session, name: str):
        return db.query(Unit).filter(Unit.name == name).first()


unit = CrudUnit(Unit)
