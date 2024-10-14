import datetime
from typing import List

from pydantic import BaseModel, ConfigDict

from schemas import RuleDB


class RiskIndexSchema(BaseModel):
    rule_id: int
    from_date: datetime.date
    to_date: datetime.date

class RiskIndexDay(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: datetime.date
    risk_index: int

class RiskIndexResponse(BaseModel):
    rule: RuleDB
    risk_index_per_day: List[RiskIndexDay]
