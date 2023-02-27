from typing import List
from fastapi import Depends, APIRouter, Request

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth.security import authorization

from app.core.schemas import SchemaSearch
from app.models.link import ControllerLink


router = APIRouter()


@router.get("/search", response_model=List[SchemaSearch])
def get_all(
        request: Request,
        offset: int = 0,
        limit: int = 10,
        sort_by: str = 'id',
        order_by: str = 'desc',
        title: str = '',
        author: str = '',
        keywords: str = '',
        db: Session = Depends(get_db),
        user=Depends(authorization)):
    return ControllerLink(db=db).read(
        offset=offset,
        limit=limit,
        sort_by=sort_by,
        order_by=order_by,
        qtype='all',
        params=request.query_params._dict)
