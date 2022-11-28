from typing import Dict, Any, Optional, Union

from sqlalchemy.orm import Session

from core import security
from crud.base import CRUDBase
from models import User
from schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """
        根据用户名返回用户信息
        :param db:
        :param username:
        :return:
        """
        return db.query(User).filter_by(username=username).first()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        """
        创建用户
        :param db:
        :param obj_in:
        :return:
        """
        db_obj = User(
            username=obj_in.username,
            hashed_password=security.get_hashed_password(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        """
        更新用户信息
        :param db:
        :param db_obj:
        :param obj_in:
        :return:
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if update_data["password"]:
            hashed_password = security.get_hashed_password(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def authenticate(self, db: Session, username: str, password: str) -> Optional[User]:
        """
        用户鉴权
        :param db:
        :param username:
        :param password:
        :return:
        """
        user = self.get_by_username(db, username)
        if not user:
            return None
        if not security.verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active


user = CRUDUser(User)
