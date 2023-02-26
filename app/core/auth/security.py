from fastapi import status, Depends, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.auth.base import BaseAuth
from app.core.auth.models.auth_user import ControllerAuthUser
from app.core.database import get_db


security = HTTPBearer()
auth_handler = BaseAuth()


async def authorization(
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials

    if not auth_handler.decode_token(token=token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"})

    return ControllerAuthUser(db=db).read(
        params={"id": auth_handler.decode_token(token=token)})
