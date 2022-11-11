from datetime import timedelta
from typing import Any
from pydantic import EmailStr

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.models.user import User as Usermodel
from app.crud.crud_user import User_instance
from app.api.api_v1 import debs
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.core.utils import (generate_password_reset_token,
                            verify_password_reset_token)

router = APIRouter(prefix='/auth2')


@router.post('/login/access-token')
def login_access_token(db: Session = Depends(debs.get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token from future requests
    :param db:
    :param form_data:
    :return:
    """
    user = User_instance.authenticate(db, form_data.username, password_attempt=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    elif not User_instance.is_active(user):
        raise HTTPException(status_code=400,
                            detail='Inactive User')
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    return {
        "access_token": security.create_access_token(user.id, expires_delta=access_token_expires),
        "token_type": "bearer"
    }


@router.post('/test-token')
def test_token(current_user: Usermodel = Depends(debs.get_current_user)) -> Any:
    """
    test access token
    :param current_user:
    :return:
    """
    return current_user


@router.post('/password-recovery/{email}')
def recover_password(email: EmailStr, db: Session = Depends(debs.get_db)) -> Any:
    """
    Password Recovery
    :param email:
    :param db:
    :return:
    """
    user = User_instance.get_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404,
                            detail='user with this username does not exist')
    password_reset_token = generate_password_reset_token(email)
    return password_reset_token


@router.post('/reset-password')
def reset_password(
        token: str = Body(...),
        new_password: str = Body(...),
        db: Session = Depends(debs.get_db),
) -> Any:
    """
    Reset Password
    :param token:
    :param new_password:
    :param db:
    :return:
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=404,
                            detail="User with this username does not exist!")
    user = User_instance.get_by_email(db, email=email)
    password = get_password_hash(new_password)
    user.password = password
    db.add(user)
    db.commit()
    return {'msg: Password updated successfully'}
