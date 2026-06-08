from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from auth import decode_token
import jwt

# OAuth2PasswordBearer is a class that implements the OAuth2 password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Get current user from token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        return decode_token(token)
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )