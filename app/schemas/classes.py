from typing import Optional
from pydantic import BaseModel


class ClassroomBase(BaseModel):
    class_id: int
    class_teacher: int


class ClassRoomCreate(ClassroomBase):
    pass


class ClassRoomUpdate(ClassroomBase):
    pass


class ClassRoomResponse(ClassroomBase):
    created_at: str

    class Config:
        orm_mode = True
