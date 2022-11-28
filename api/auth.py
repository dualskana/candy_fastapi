from datetime import timedelta

from fastapi import APIRouter, HTTPException
from fastapi.params import *
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
from api import deps
import schemas
from core import security
from core.config import settings

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
async def login(db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.user.authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return schemas.Token(access_token=security.create_access_token(user.username, access_token_expires),
                         token_type="bearer", )
