from pydantic import BaseModel


class TalkRequest(BaseModel):
    message: str