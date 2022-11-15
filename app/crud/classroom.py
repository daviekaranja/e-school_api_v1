import logging
from typing import List, Any

from fastapi.encoders import jsonable_encoder
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import exc

from app.api.api_v1 import debs
from app.crud.base import CrudBase
from app.models.classes import ClassRoom
from app.models.user import User
from app.schemas.institutions import SchoolCreate, SchoolUpdate
from app.schemas.classes import ClassRoomCreate, ClassRoomUpdate

logger = logging.getLogger(__name__)


class CRUDClassRoom(CrudBase[ClassRoom, ClassRoomCreate, ClassRoomUpdate]):
    def create_with_school(self, db: Session, school_id: int, obj_in: ClassRoomCreate) -> Any:
        """
        create a class with school
        :param db:
        :param school_id:
        :param obj_in:
        :return:
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, class_id=school_id)
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except exc.SQLAlchemyError as error:
            logger.error(error, exc_info=True)
            return None

    def get_by_school(self, db: Session, school_id: int) -> List[ClassRoom]:
        """
        get all classrooms that belong to a school
        :param db:
        :param school_id:
        :return:
        """
        classes = db.query(self.model).filter(ClassRoom.class_id == school_id).all()
        return classes
