from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .institutions import Institution

"""
This should give details about 
"""


class Teacher(Base):
    teacher_id = Column(Integer, ForeignKey('institution.school_id'), primary_key=True)
    school = relationship('Institution', back_populates='teachers')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
