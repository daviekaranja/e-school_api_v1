from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .institutions import Institution


class ClassRoom(Base):
    class_id = Column(Integer, ForeignKey('institution.school_id'), primary_key=True)
    class_teacher = Column(Integer, ForeignKey('teacher.teacher_id'))
    school = relationship('Institution', back_populates='classes')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
