from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    UniqueConstraint,
    ForeignKey)
from app.core.database import Base
from app.models.link import Link


class LinkConnection(Base):
    __tablename__ = "link_connection"
    __table_args__ = (
        UniqueConstraint('id_link', 'id_href', name='unique_component_commit'),
    )

    id = Column(Integer, primary_key=True, index=True)
    id_link = Column(Integer, ForeignKey(Link.id), index=True)
    id_href = Column(Integer, ForeignKey(Link.id), index=True)
    status = Column(Boolean, default=True)
