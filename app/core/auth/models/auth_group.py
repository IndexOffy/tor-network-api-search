from sqlalchemy import (
    Column,
    String,
    Integer)
from app.core.database import Base
from app.core.controller import BaseController


class AuthGroup(Base):
    """Model Auth Groups
    """

    __tablename__ = "auth_group"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(75), unique=True)


class ControllerAuthGroup(BaseController):

    def __init__(self, db = None):
        super().__init__(db)
        self.model_class = AuthGroup
