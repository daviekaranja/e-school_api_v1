from typing import Optional
from .user import User

from pydantic import BaseModel, EmailStr


class SchoolBase(BaseModel):
    school_name: Optional[str] = None
    email: EmailStr
    is_active: bool = True


class SchoolCreate(SchoolBase):
    pass


class SchoolUpdate(SchoolBase):
    pass


class SchoolInDBBase(SchoolBase):
    school_id: int
    school_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class School(SchoolInDBBase):
    pass


class ResponseModel(School):
    owner: User

    class Config:
        orm_mode = True
