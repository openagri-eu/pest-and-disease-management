from typing import List

from pydantic import BaseModel, ConfigDict


class CreateOperator(BaseModel):
    symbol: str


class UpdateOperator(BaseModel):
    symbol: str


class OperatorDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    symbol: str


class Operators(BaseModel):
    operators: List[OperatorDB]
