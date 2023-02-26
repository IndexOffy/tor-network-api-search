from typing import Optional
from pydantic import BaseModel, EmailStr, SecretStr


class SchemaSignup(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    password: SecretStr


class SchemaLogin(BaseModel):
    access_token: str
    refresh_token: str


class SchemaRefreshToken(BaseModel):
    access_token: str
