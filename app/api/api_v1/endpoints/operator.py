from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
from api import deps
from models import User
from schemas import Operators

router = APIRouter()

@router.get("/", response_model=Operators)
def get_all_operators(
        db: Session = Depends(deps.get_db),
        user: User = Depends(deps.get_current_user)
) -> Operators:
    """
    Returns all operators that can be used.
    """

    operators_db = crud.operator.get_all(db=db)

    return Operators(operators=operators_db)
