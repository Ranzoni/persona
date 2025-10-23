from typing import Any
from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool
    source: Any

class TalkRequest(BaseModel):
    message: str

class PersonaRequest(BaseModel):
    name: str
    prompt: str