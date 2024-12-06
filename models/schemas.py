from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class FolloweesResponse(BaseModel):
    username: str
    full_name: str
    profile_pic_url: str

class PostDownloadResponse(BaseModel):
    username: str
    post_url: str
    shortcode: str
    caption: str
    likes: int
    comments: int
    media_url: str

class ProfileResponse(BaseModel):
    username: str
    full_name: str
    profile_pic_url: str
    biography: str