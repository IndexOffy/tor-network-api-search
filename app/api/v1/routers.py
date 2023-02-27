from fastapi import APIRouter
from app.api.v1.endpoints import search

router = APIRouter()
router.include_router(search.router, tags=["Search"])
