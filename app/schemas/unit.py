from typing import List

from pydantic import BaseModel, ConfigDict


class UnitCreate(BaseModel):
    symbol: str


class UnitUpdate(BaseModel):
    symbol: str


class Unit(BaseModel):
    id: int
    symbol: str


class UnitDelete(BaseModel):
    id: int


class Units(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    units: List[Unit]
