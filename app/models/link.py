import logging

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime)
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
    created_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ControllerLink(BaseController):

    def __init__(self, db=None):
        super().__init__(db)
        self.model_class = Link

    def read(
            self,
            offset: int = 0,
            limit: int = 10,
            sort_by: str = 'id',
            order_by: str = 'desc',
            qtype: str = 'first',
            params: dict = {},
            **kwargs):
        """Get a record from the database.
        """
        self.load_columns(params)
        limit = limit if limit <= 10 else 10

        try:
            query_model = self.db.query(self.model_class)
            for column in self.columns:
                query_model = query_model.filter(
                    getattr(self.model_class, column).like(f"%{self.columns.get(column)}%"))

            sort_by = getattr(self.model_class, sort_by)

            return getattr(query_model.order_by(
                getattr(sort_by, order_by)()).offset(offset).limit(limit), qtype)()

        except Exception as error:
            logging.error(error)

        finally:
            if self.close_session:
                self.db.close()
