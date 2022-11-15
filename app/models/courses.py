from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Courses(Base):
    course_id = Column(Integer, primary_key=True, nullable=False)
    course_name = Column(String(30), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
