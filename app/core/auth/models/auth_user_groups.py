from sqlalchemy import (
    Column,
    Integer,
    ForeignKey)
from app.core.database import Base, engine
from app.core.controller import BaseController
from app.core.auth.models import AuthUser, AuthGroup


class AuthUserGroup(Base):
    """Model Auth User Groups
    """

    __tablename__ = "auth_user_groups"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(AuthUser.id))
    group_id = Column(Integer, ForeignKey(AuthGroup.id))


class ControllerAuthUserGroup(BaseController):

    def __init__(self, db=None):
        super().__init__(db)
        self.model_class = AuthUserGroup


Base.metadata.create_all(bind=engine)
