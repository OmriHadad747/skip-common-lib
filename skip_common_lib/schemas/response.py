from typing import Any
from pydantic import BaseModel


class MsgResponse(BaseModel):
    args: dict[str, Any]
    msg: str