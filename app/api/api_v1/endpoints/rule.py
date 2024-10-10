from fastapi import APIRouter, HTTPException, Depends
from requests import Session

import crud
from api import deps
from schemas import Message, RulesDB, RuleDB, CreateRule, CreateCondition

router = APIRouter()


@router.post("/", response_model=RuleDB)
def create_rule(
        rule: CreateRule,
        db: Session = Depends(deps.get_db)
):
    """
    Create a rule such as: temperature > 50 AND air_pressure < 20 AND humidity < 50
    """

    if rule.from_time > rule.to_time:
        raise HTTPException(
            status_code=400,
            detail="Times value mismatch, switch them."
        )

    if len(rule.conditions) == 0:
        raise HTTPException(
            status_code=400,
            detail="Can't create rule with no conditions."
        )

    # Check whether there are two conditions with the same unit
    # TODO: include rules that contain a > 5 and a < 10 as conditions
    cond_times = {}
    for cond in rule.conditions:
        # Count for same conditions present in file
        if not cond.unit_id in cond_times:

            # Check for unit and operator ids
            operator_db = crud.operator.get(db=db, id=cond.operator_id)
            if not operator_db:
                raise HTTPException(
                    status_code=400,
                    detail="Operator with ID: {} does not exist.".format(cond.operator_id)
                )
            unit_db = crud.unit.get(db=db, id=cond.unit_id)
            if not unit_db:
                raise HTTPException(
                    status_code=400,
                    detail="Unit with ID: {} does not exist.".format(cond.unit_id)
                )

            cond_times[cond.unit_id] = [cond.unit_id]
            continue
        cond_times[cond.unit_id].append(cond.unit_id)

        # Check for unit and operator ids
        operator_db = crud.operator.get(db=db, id=cond.operator_id)
        if not operator_db:
            raise HTTPException(
                status_code=400,
                detail="Operator with ID: {} does not exist.".format(cond.operator_id)
            )
        unit_db = crud.unit.get(db=db, id=cond.unit_id)
        if not unit_db:
            raise HTTPException(
                status_code=400,
                detail="Unit with ID: {} does not exist.".format(cond.unit_id)
            )

    for cond in cond_times.values():
        if len(cond) >= 2:
            raise HTTPException(
                status_code=400,
                detail="Can't have more that one condition per unit."
            )

        # Find way to parse rules from schema to only disallow truly impossible rules (i.e. a == 5, a == 10 | a != 5, a != 10, a == 5 | ...

        # if len(cond) >= 3:
        #     raise HTTPException(
        #         status_code=400,
        #         detail="Can't have more that two conditions per unit."
        #     )

        # if len(cond) == 1:
        #     continue
        #
        # conditions_in_question = [cond_q for cond_q in rule.conditions if cond_q.unit_id == cond[0]]
        # operators_db = crud.operator.get_all(db=db)
        # not_allowed = [crud.operator.get_by_symbol(db=db, symbol="=="), crud.operator.get_by_symbol(db=db, symbol="!=")]
        # if any([x in not_allowed for x in conditions_in_question]):
        #     raise HTTPException(
        #         status_code=400,
        #         detail="Can't have multiple conditions that use != or == as "
        #     )

    rule_db = crud.rule.create(db=db, obj_in=rule)

    for cond in rule.conditions:
        crud.condition.create(db=db, obj_in=CreateCondition(**cond.model_dump(), rule_id=rule_db.id))

    return rule_db



@router.get("/", response_model=RulesDB)
def get_all_rules(
        db: Session = Depends(deps.get_db)
):
    """
    Returns all stored rules.
    """

    rules_db = crud.rule.get_all(db=db)

    return RulesDB(rules=rules_db)


@router.delete("/{rule_id}", response_model=RuleDB)
def delete_rule(
        rule_id: int,
        db: Session = Depends(deps.get_db)
) -> Message:
    """
    Delete a rule
    """

    rule_db = crud.rule.get(db=db, id=rule_id)

    if not rule_db:
        raise HTTPException(
            status_code=400,
            detail="Can't delete rule that doesn't exist."
        )

    rule_db = crud.rule.remove(db=db, id=rule_id)

    return rule_db
