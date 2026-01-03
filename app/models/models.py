from sqlalchemy import Column, String

from app.models.base import BaseMixin, Base


class User(BaseMixin, Base):
    __tablename__ = "users"

    name = Column(String, nullable=False, unique=False)
    email = Column(String, nullable=False, unique=True)
    avatar_url = Column(String, nullable=False, unique=True)
    provider = Column(String, nullable=False, unique=False)
    provider_id = Column(String, nullable=False, unique=True)
