from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    password: str


class UserMe(BaseModel):
    email: str

    class Config:
        from_attributes = True

