from pydantic import BaseModel


class Post(BaseModel):
    id: int
    page_name: str
    content: str
    replies: list
    like: list


class Page(BaseModel):
    id: int
    owner: str
    owner_email: str
    tags: list
    followers: list
    following: list
    name: str
    follow_requests: list
