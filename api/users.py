from fastapi import APIRouter, HTTPException
from fastapi.params import *
from sqlalchemy.orm import Session

import crud
from api import deps
import models
import schemas

router = APIRouter()


@router.get("/{username}", response_model=schemas.BaseResp[Optional[schemas.User]])
async def get_user_by_username(username: str,
                               current_user: models.User = Depends(deps.get_current_user),
                               db: Session = Depends(deps.get_db)):
    return schemas.BaseResp(code=0, msg="", data=crud.user.get_by_username(db, username))


@router.post("/create", response_model=schemas.BaseResp[schemas.User])
async def create_user(user_in: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    print(user_in)
    user = crud.user.get_by_username(db, user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, user_in)
    return schemas.BaseResp(code=0, msg="", data=user)
