import traceback

from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import Rule, Condition
from schemas import CreateRule, UpdateRule


class CrudRule(CRUDBase[Rule, CreateRule, UpdateRule]):

    def get_all(self, db: Session):
        return db.query(Rule).all()


rule = CrudRule(Rule)
