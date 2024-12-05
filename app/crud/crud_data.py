import datetime
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, Query
from crud.base import CRUDBase
from models import Data
from schemas import CreateData


class CrudData(CRUDBase[Data, CreateData, dict]):

    def get_all(self, db: Session):
        return db.query(Data).all()

    def get_data_query_by_dataset_id(self, db: Session, dataset_id: int) -> Query:
        query = db.query(Data).filter(Data.dataset_id == dataset_id).order_by(Data.date.asc(), Data.time.asc())
        return query

    def batch_insert(self, db: Session, rows: List[CreateData]) -> Optional[List[Data]]:
        rows_model = [Data(**x.model_dump()) for x in rows]

        db.add_all(rows_model)
        try:
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            return None

        [db.refresh(x) for x in rows_model]

        return rows_model


data = CrudData(Data)
