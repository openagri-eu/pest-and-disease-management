from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models import Condition
from schemas import CreateCondition


class CrudCondition(CRUDBase[Condition, CreateCondition, dict]):

    def get_all(self, db: Session):
        return db.query(Condition).all()


condition = CrudCondition(Condition)
