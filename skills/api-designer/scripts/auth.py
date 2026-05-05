from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
import jwt
import os

security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY")


def get_current_user(token=Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
