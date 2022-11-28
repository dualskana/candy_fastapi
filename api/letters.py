from typing import List

from fastapi import APIRouter
from fastapi.params import *
from sqlalchemy.orm import Session

import crud
import models
import schemas
from api import deps

router = APIRouter()


@router.post("/create", response_model=schemas.BaseResp[schemas.Letter])
async def create_letter(letter_in: schemas.LetterCreate, db: Session = Depends(deps.get_db),
                        current_user: models.User = Depends(deps.get_current_user)):
    letter = crud.letter.create(db, obj_in=letter_in, user_id=current_user.id)
    letter.author = current_user
    return schemas.BaseResp(code=0, msg="", data=letter)


@router.post("/{user_id}", response_model=schemas.BaseResp[List[schemas.Letter]])
async def get_all_by_user_id(user_id: int, page: int = Body(default=0), size: int = Body(default=10),
                             db: Session = Depends(deps.get_db),
                             current_user: models.User = Depends(deps.get_current_user)):
    skip = page * size
    limit = size
    res = crud.letter.get_letter_by_user_id(db, user_id=user_id, skip=skip, limit=limit)
    return schemas.BaseResp(code=0, msg="", data=res)
