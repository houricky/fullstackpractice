from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from dependencies import get_current_user
from models import Token, User
from user_services import authenticate_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form.username, form.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    from auth import create_access_token
    token = create_access_token(user.username)
    return Token(access_token=token)


@router.get("/me", response_model=User)
def read_me(username: str = Depends(get_current_user)):
    from user_services import get_user_by_username
    doc = get_user_by_username(username)
    return User(id=doc["id"], username=doc["username"])