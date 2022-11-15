from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .institutions import Institution

"""
This should give details about 
"""


class Students(Base):
    student_id = Column(Integer, index=True, primary_key=True)
    school_id = Column(Integer, ForeignKey('institution.school_id'))
    classroom = Column(Integer, ForeignKey('classroom.class_id'), unique=True)
    # school = relationship('Institution', back_populates='classes')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
