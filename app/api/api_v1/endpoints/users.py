from typing import Any, List

from fastapi import APIRouter, HTTPException, status, Body, Depends
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import exc

from app.crud import crud_user
from app.crud.crud_user import User_instance
from app.core.config import settings
from app.schemas import user as user_schema
from app import crud, models
from app.api.api_v1 import debs
from app.models.user import User as UserModel

router: APIRouter = APIRouter()


@router.get('/')
def get_users(db: Session = Depends(debs.get_db), skip: int = 0, limit: int = 100, current_user: UserModel = Depends(debs.get_current_active_superuser)) -> List[UserModel]:
    """
    retrieve multiple users
    :param current_user:
    :param db:
    :param skip:
    :param limit:
    :return:
    """
    try:
        users = User_instance.get_multiple(db, skip, limit)
    except exc.SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=error)

    return users


@router.get('/{user_id}')
def get_user(user_id: int, db: Session = Depends(debs.get_db), skip: int = 0, limit: int = 100):
    """
    get a user based on the id
    :param user_id:
    :param db:
    :param skip:
    :param limit:
    :return:
    """
    try:
        user = crud_user.User_instance.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'user with id[{user_id}] does not exist!')
        return user
    except exc.SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=jsonable_encoder(error))


@router.post('/', status_code=status.HTTP_201_CREATED)
def add_user(user_in: user_schema.UserCreate, db: Session = Depends(debs.get_db)):
    """
    Create New User.
    :param user_in:
    :param db:
    :return:
    """
    user = crud_user.User_instance.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='the user with this username already exist in the database!')

    user = crud_user.User_instance.create(db, obj_in=user_in)
    return user


@router.put('/{user_id}', status_code=status.HTTP_201_CREATED)
def update_user(
        *,
        db: Session = Depends(debs.get_db),
        user_id: int,
        user_in: user_schema.UserUpdate,

) -> Any:
    """
    Update user
    :param user_id:
    :param user_in:
    :param db:
    :return:
    """
    user = crud_user.User_instance.get_by_id(db, obj_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The User with this username does not exist'
        )
    user = crud_user.User_instance.update_user(db, db_obj=user, obj_in=user_in)
    return user


@router.put('/me', status_code=status.HTTP_201_CREATED)
def update_current_user(
        db: Session = Depends(debs.get_db),
        password: str = Body(None),
        full_name: str = Body(None),
        email: EmailStr = Body(None),
        current_user: UserModel = Depends(debs.get_current_user)
) -> Any:
    """
    update own user
    :param db:
    :param password:
    :param full_name:
    :param email:
    :param current_user:
    :return:
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = user_schema.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user_update = crud_user.User_instance.update_user(db, db_obj=current_user, obj_in=user_in)
    return user_update
