from datetime import datetime
from typing import Optional

from pydantic import BaseModel

import models
import schemas


class LetterBase(BaseModel):
    text: str
    images: Optional[str] = None
    audio: Optional[str] = None
    video: Optional[str] = None
    type: int


class LetterCreate(LetterBase):
    pass


class LetterUpdate(LetterBase):
    pass


class Letter(LetterBase):
    id: int
    author_id: int
    create_time: datetime
    author: schemas.User

    class Config:
        orm_mode = True
