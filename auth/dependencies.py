# OAuth2 password bearer dependency
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM
from models.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from database_configs.db import get_db
from crud.crud_user import get_user_by_email


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/oauth2-login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user