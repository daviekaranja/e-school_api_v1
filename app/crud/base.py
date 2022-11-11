import logging
from typing import TypeVar, Dict, Generic, List, Optional, Type, Union, Any

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import exc

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)  # a sqlalchemy models, response model
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

logger = logging.getLogger(__name__)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __int__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `models`: A SQLAlchemy models class
        * `schema`: A Pydantic models (schema) class
        :param model:
        :return:
        """
        self.model = model

    # get single user
    def get_user(self, db: Session, obj_id: Any) -> Optional[ModelType]:
        try:
            user = db.query(self.model).filter(self.model.id == obj_id).first()
            return user
        except exc.SQLAlchemyError as error:
            logger.error(msg='Operation Failed', exc_info=True)
            raise error

    # get users
    def get_multiple(self, db: Session, *, skip: int = 0, limit: int = 100
                     ) -> List[ModelType]:
        try:
            user = db.query(self.model).offset(skip).limit(limit).all()
            return user
        except exc.SQLAlchemyError as error:
            raise error

    # create user
    def create_user(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except exc.SQLAlchemyError as error:
            raise error

    # update
    def update(self, *, db: Session, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]],
               ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in obj_data:
                setattr(db_obj, field, update_data[field])
                try:
                    db.add(db_obj)
                    db.commit()
                    db.refresh(db_obj)
                    return db_obj
                except exc.SQLAlchemyError as error:
                    raise error

    # delete
    def remove(self, db: Session, *, obj_id: int) -> ModelType:
        obj = db.query(self.model).get(obj_id)
        try:
            db.delete(obj)
            db.commit()
            return obj
        except exc.SQLAlchemyError as error:
            raise error


class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    default object with full CRUD functionality(Create, Read, Update, Delete)
    param: Create schema,
    param: Update schema,

    """

    def __init__(self, model: Type[ModelType]):
        self.model = model  # model class being queried

    def get_by_id(self, db: Session, obj_id: Any) -> Optional[ModelType]:
        """
        get by id!
        :param obj_id:
        :param db:
        :return:
        """
        try:
            db_obj = db.query(self.model).filter(self.model.id == obj_id).first()
            return db_obj
        except exc.SQLAlchemyError as error:
            logger.error(msg='operation failed!', exc_info=error)
            raise error

    def get_multiple(self, db: Session, skip: int = 0, limit: int = 100) -> list[ModelType]:
        """
        get multiple objects!
        :param db:
        :param skip:
        :param limit:
        :return:
        """
        try:
            obj = db.query(self.model).offset(skip).limit(limit).all()
            return obj
        except exc.SQLAlchemyError as error:
            logger.error(msg='operation failed', exc_info=error)
            raise error

    def create_object(self, db: Session, *, new_object: CreateSchemaType):
        """
        create a new object
        :param new_object:
        :param db: a database session
        :param new_object: a schema
        :return:
        """
        new_object_data = self.model(**new_object)
        db.add(new_object_data)
        try:
            db.commit()
            db.refresh(new_object_data)
            return new_object_data
        except exc.SQLAlchemyError as error:
            logger.error(msg='operation failed', exc_info=error)
            raise error

    def update_object(self, db: Session, db_object: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> \
            Optional[ModelType]:
        """
        update a user
        :param db_object:
        :param db:
        :param obj_in: update schema
        :return:
        """
        obj_data = jsonable_encoder(db_object)  # updated data
        if isinstance(obj_in, dict):
            # checks if all the fields have been updated
            update_data = obj_in

        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_object, field, update_data[field])
        try:
            db.add(db_object)
            db.commit()
            db.refresh(db_object)
            return db_object
        except exc.SQLAlchemyError as error:
            logger.error('Operation Failed!', exc_info=True)
            return None

    def delete_object(self, db: Session, obj_id: int):
        obj_query = db.query(self.model).filter(self.model.id == obj_id)
        if obj_query.first() is None:
            raise Exception('user does not exist!')
        obj_query.delete(synchronize_session=False)
        try:
            db.commit()
        except exc.SQLAlchemyError as error:
            raise Exception(str(error))
