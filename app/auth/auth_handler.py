import os
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
token_exiration = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=token_exiration)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    except ExpiredSignatureError:
        return None
