from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from models import User
from crud import user

from core import security
from core.config import settings
from db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token/")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.KEY, algorithms=[security.ALGORITHM]
        )
        # token_data = TokenPayload(**payload)
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    # user_db = user.get(db, id=token_data.sub)
    user_db = user.get(db, id=payload["sub"])
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db


def get_administrator(
        db: Session = Depends(get_db),
        token: str = Depends(reusable_oauth2)
) -> User:
    user_db = get_current_user(db=db, token=token)

    if user_db.role.name != "Admin":
        raise HTTPException(
            status_code=401, detail="User not authorized"
        )

    return user_db
