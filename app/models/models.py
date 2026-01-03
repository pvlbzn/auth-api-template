from sqlalchemy import Column, String, UUID

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    name = Column(String, nullable=False, unique=False)
    email = Column(String, nullable=False, unique=True)
    provider_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
