from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .institutions import Institution


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    schools_by_user = relationship('Institution', back_populates='owner')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
