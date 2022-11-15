from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User
    from .classes import ClassRoom
    from .teachers import Teacher


class Institution(Base):
    school_id = Column(Integer, primary_key=True, index=True)
    school_name = Column(String, index=True, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean(), default=True)
    principal = Column(Integer, nullable=False, default=1)
    school_admin = Column(Integer, ForeignKey('user.id'))

    # relationships
    owner = relationship('User', back_populates='schools_by_user')
    classes = relationship('ClassRoom', back_populates='school')
    teachers = relationship('Teacher', back_populates='school')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
