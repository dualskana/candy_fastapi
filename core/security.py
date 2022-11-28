from datetime import datetime, timedelta
from typing import Any, Union

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from core.config import settings

pwd_content = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    """
    校验密码
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_content.verify(plain_password, hashed_password)


def get_hashed_password(password):
    """
    获取哈希密码
    :param password:
    :return:
    """
    return pwd_content.hash(password)


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    创建JWT Token
    :param subject:
    :param expires_delta:
    :return:
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
