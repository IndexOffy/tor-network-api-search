from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean)
from datetime import datetime
from app.core.controller import BaseController
from app.core.database import Base


class Link(Base):
    __tablename__ = "link"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    link = Column(String(95), unique=True, index=True)
    title = Column(String(100))
    author = Column(String(45))
    keywords = Column(String(50))
    verify = Column(Boolean, default=False, index=True)
    explored = Column(Boolean, default=False, index=True)
    running = Column(Boolean, default=False, index=True)
    fail = Column(Boolean, default=False)
    login = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)
    created_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ControllerLink(BaseController):

    def __init__(self, db=None):
        super().__init__(db)
        self.model_class = Link
