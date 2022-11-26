from typing import Any
from pydantic import BaseModel


class MsgResponse(BaseModel):
    args: dict[str, Any]
    msg: str


class EntityResponse(BaseModel):
    entity: dict[str, Any]