import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class Condition(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    unit_id: int
    operator_id: int
    value: float


class CreateCondition(BaseModel):
    rule_id: int
    unit_id: int
    operator_id: int
    value: float


class CreateRule(BaseModel):
    name: str
    description: Optional[str] = None

    from_time: datetime.time
    to_time: datetime.time


class CreateRuleWithConditions(CreateRule):
    conditions: List[Condition] = []


class UpdateRule(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    from_time: Optional[datetime.time] = None
    to_time: Optional[datetime.time] = None

    conditions : Optional[List[Condition]] = []


class RuleDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    name: str
    description: Optional[str] = None

    from_time: datetime.time
    to_time: datetime.time

    conditions: List[Condition] = []


class RulesDB(BaseModel):
    rules: List[RuleDB] = []


class Rule(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: Optional[str] = None

    from_time: datetime.time
    to_time: datetime.time

    conditions: List[Condition] = []
