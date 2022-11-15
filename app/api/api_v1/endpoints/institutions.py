from typing import Any, List

from fastapi import APIRouter, HTTPException, status, Body, Depends
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import exc

from app.api.api_v1 import debs
from app.models.institutions import Institution
from app.models.user import User
from app.crud.institution import school
from app.schemas.institutions import SchoolCreate, ResponseModel, School

router = APIRouter(prefix='/institutions')


@router.get('/', response_model=List[ResponseModel])
def get_institutions(
        db: Session = Depends(debs.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: User = Depends(debs.get_current_active_superuser)
) -> List[Institution]:
    schools = school.get_multiple(db=db, skip=skip, limit=limit)
    if not schools:
        raise HTTPException(status_code=404, detail='not found!')
    return schools


@router.get('/schools-by-owner')
def get_by_owner(db: Session = Depends(debs.get_db), skip: int = 0, limit: int = 100,
                 current_user: User = Depends(debs.get_current_active_user)):
    schools = school.get_multi_by_owner(db=db, owner_id=current_user.id, skip=skip, limit=limit)
    if not schools:
        raise HTTPException(status_code=404, detail='Not Found!')
    return schools


@router.post('/', status_code=201)
def create_institution(data: SchoolCreate,
                       db: Session = Depends(debs.get_db),
                       current_user: User = Depends(debs.get_current_active_user)) -> Any:
    """
    create new institution
    :param data:
    :param db:
    :param current_user:
    :return:
    """
    schol = school.create_with_owner(
        db=db, owner_id=current_user.id, obj_in=data
    )
    return schol
