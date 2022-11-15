from typing import Any, Dict, Optional, Union
import logging

from sqlalchemy.orm import Session
from sqlalchemy import exc

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase, CrudBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

logger = logging.getLogger(__name__)


class CrudUser(CrudBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        get a user by email
        :param db:
        :param email:
        :return:
        """
        try:
            user = db.query(User).filter(User.email == email).first()
            return user
        except exc.SQLAlchemyError as error:
            logger.error(msg='Operation failed', exc_info=True)
            raise Exception(str(error))

    def create(self, db: Session, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_user(self, db: Session, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        password = update_data.get('password', None)
        if password is not None:
            hashed_password = get_password_hash(password)
            del update_data['password']
            update_data[password] = hashed_password
        return super().update_object(db, db_object=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, email: str, password_attempt: str) -> Optional[User]:
        curret_user = self.get_by_email(db, email=email)
        if not curret_user:
            return None
        if not verify_password(password_attempt, hashed_password=curret_user.password):
            return None
        return curret_user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User):
        return user.is_superuser


User_instance = CrudUser(User)
