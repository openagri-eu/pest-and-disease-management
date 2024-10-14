import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api import deps
from schemas import RiskIndexResponse

from crud import rule, data

import pandas as pd

router = APIRouter()

@router.get("/calculate-risk-index/{rule_id}", response_model=RiskIndexResponse)
def calculate_risk_index(
    rule_id: int,
    from_date: datetime.date,
    to_date: datetime.date,
    db: Session = Depends(deps.get_db)
):
    """
    Return risk index associated data for frontend to render.
    """

    rule_db = rule.get(db=db, id=rule_id)

    if not rule_db:
        raise HTTPException(
            status_code=400,
            detail="Rule with id: {} does not exist.".format(rule_id)
        )

    if from_date > to_date:
        raise HTTPException(
            status_code=400,
            detail="From and To dates are mismatched, please swap them."
        )

    # SQL query for the data
    data_db = data.get_data_interval_query(
        db=db,
        from_date=from_date,
        to_date=to_date,
        rule_from_time=rule_db.from_time,
        rule_to_time=rule_db.to_time
    )

    df = pd.read_sql(sql=data_db.statement, con=db.bind, parse_dates={"date": "%Y-%m-%d"})

    conds = []
    for cond in rule_db.conditions:
        conds.append("(x['{}'] {} {})".format(cond.unit.name, cond.operator.symbol, float(cond.value)))
    pre_final_str = ""
    for cond_strs in conds[:len(conds) - 1]:
        pre_final_str = pre_final_str + cond_strs + " & "
    final_str = pre_final_str + conds[-1]

    l_f = "lambda x: {}".format(final_str)

    l_f_e = eval(l_f)

    df = df.assign(risk=l_f_e)

    groups = df.groupby("date")["risk"].mean()

    l = [{"risk_index": int(a * 100), "date":b.date()} for a,b in zip(groups.tolist(), groups.index.tolist())]
    return RiskIndexResponse(rule=rule_db, risk_index_per_day=l)
