from typing import TypeVar, Generic

from pydantic.generics import GenericModel

T = TypeVar("T")


class BaseResp(GenericModel, Generic[T]):
    code: int
    msg: str
    data: T
