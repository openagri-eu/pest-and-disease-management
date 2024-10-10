from sqlalchemy.orm import Session
from crud.base import CRUDBase

from models import Operator
from schemas import CreateOperator, UpdateOperator


class CrudOperator(CRUDBase[Operator, CreateOperator, UpdateOperator]):

    def get_all(self, db: Session):
        return db.query(Operator).all()

    def get_by_symbol(self, db: Session, symbol: str):
        return db.query(Operator).filter(Operator.symbol == symbol).first()


operator = CrudOperator(Operator)
