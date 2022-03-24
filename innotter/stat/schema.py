from pydantic import BaseModel


class MessageSchema(BaseModel):
    message: str


class TestSchema(BaseModel):
    test: dict


class PageSchema(BaseModel):
    id: int
    owner: str
    owner_email: str
    tags: list
    followers: list
    following: list
    name: str
    follow_requests: list
