import logging
from typing import List, Any

from fastapi.encoders import jsonable_encoder
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import exc

from app.api.api_v1 import debs
from app.crud.base import CrudBase
from app.models.institutions import Institution
from app.models.user import User
from app.schemas.institutions import SchoolCreate, SchoolUpdate
from app.schemas.classes import ClassRoomCreate, ClassRoomUpdate

logger = logging.getLogger(__name__)


class CRUDSchool(CrudBase[Institution, SchoolCreate, SchoolUpdate]):
    def create_with_owner(self, db: Session, owner_id: int, obj_in: SchoolCreate) -> Any:
        """
        create a school linked with owner
        :param db:
        :param owner_id:
        :param obj_in:
        :return:
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, school_admin=owner_id)
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except exc.SQLAlchemyError as error:
            logger.error(error, exc_info=True)
            return None

    def get_multi_by_owner(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100,
                           ) -> List[Institution]:
        schools = db.query(self.model).filter(Institution.school_admin == owner_id).offset(skip).limit(limit).all()
        return schools

    def assign_school_roles(self, roles: str| List, teacher_id: int,db: Session):
        pass


school = CRUDSchool(Institution)
