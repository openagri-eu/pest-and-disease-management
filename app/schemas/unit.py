from typing import List

from pydantic import BaseModel, ConfigDict


class UnitCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    symbol: str


class UnitUpdate(BaseModel):
    symbol: str


class Unit(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    symbol: str


class UnitDelete(BaseModel):
    id: int


class Units(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    units: List[Unit]
