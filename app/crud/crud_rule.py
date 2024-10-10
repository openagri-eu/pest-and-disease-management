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

    def create(self, db: Session, obj_in: CreateRule, **kwargs) -> Rule:
        obj_in_data = jsonable_encoder(obj_in)

        rule_obj = Rule()
        rule_obj.name = obj_in_data["name"]
        rule_obj.description = obj_in_data["description"]
        rule_obj.from_time = obj_in_data["from_time"]
        rule_obj.to_time = obj_in_data["to_time"]

        db.add(rule_obj)

        try:
            db.commit()
        except SQLAlchemyError:
            traceback.print_exc()
            return None
        db.refresh(rule_obj)

        return rule_obj


rule = CrudRule(Rule)
