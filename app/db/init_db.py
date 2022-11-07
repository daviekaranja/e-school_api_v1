from sqlalchemy.orm import Session
import logging

from app.crud import crud_user
from app.schemas.user import UserCreate
from app.core.config import settings
from app.db import base

logger = logging.getLogger(__name__)

first_superuser = settings.FIRST_SUPERUSER_EMAIL


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

def init_db(db: Session) -> None:
    if first_superuser:
        user = crud_user.user.get_by_email(db, email=first_superuser)
        if not user:
            user_in = UserCreate(
                full_name='Davie Karanja Muiruri',
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_active=True,
                is_superuser=True
            )
            user = crud_user.user.create(db, obj_in=user_in)
            logger.info("Superuser created successfully")
        else:
            logger.info(
                f"skipping creating superuser, already exist!"
            )