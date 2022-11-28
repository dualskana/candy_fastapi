from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import models
from crud.base import CRUDBase
from models.letter import Letter
from schemas.letter import LetterUpdate, LetterCreate


class CRUDLetter(CRUDBase[Letter, LetterCreate, LetterUpdate]):

    def create(self, db: Session, *, obj_in: LetterCreate, user_id: int) -> Letter:
        obj_in_data = jsonable_encoder(obj_in)
        db_letter = Letter(**obj_in_data, author_id=user_id)
        db.add(db_letter)
        db.commit()
        db.refresh(db_letter)
        return db_letter

    def get_letter_by_user_id(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 10) -> List[models.User]:
        return db.query(Letter) \
            .filter_by(author_id=user_id) \
            .order_by(Letter.create_time) \
            .offset(skip) \
            .limit(limit).all()

    def get_latest(self, db: Session, *, skip: int = 0, limit: int = 10):
        return db.query(Letter) \
            .offset(skip) \
            .limit(limit) \
            .order_by(Letter.create_time).all()


letter = CRUDLetter(Letter)
