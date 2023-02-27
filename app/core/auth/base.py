import jwt

from fastapi import HTTPException, status
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.core.settings import set_up


class BaseAuth:

    def __init__(self, config: dict = set_up()) -> None:
        self.crypt = CryptContext(schemes=["sha256_crypt", "des_crypt"])
        self.secret = config.get("SECRET_KEY")

    def encode_password(self, password):
        return self.crypt.hash(password)

    def verify_password(self, password, encoded_password):
        return self.crypt.verify(password, encoded_password)

    def encode_token(self, email):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=30),
            'iat': datetime.utcnow(),
            'scope': 'access_token',
            'value': email}

        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256')

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            if (payload['scope'] == 'access_token'):
                return payload

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Scope for the Token is Invalid')

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token Expired')

        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid Token')

    def encode_refresh_token(self, email):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, hours=10),
            'iat': datetime.utcnow(),
            'scope': 'refresh_token',
            'value': email}

        return jwt.encode(
            payload=payload,
            key=self.secret,
            algorithm='HS256')

    def refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(
                jwt=refresh_token,
                key=self.secret,
                algorithms=['HS256'])

            if (payload['scope'] == 'refresh_token'):
                email = payload['value']
                new_token = self.encode_token(email)
                return new_token

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid Scope for Token')

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Refresh Token Expired')

        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid Refresh Token')
