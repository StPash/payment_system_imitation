from pydantic import BaseModel, EmailStr


class SLoginData(BaseModel):
    email: EmailStr
    password: str


class SAccessToken(BaseModel):
    access_token: str
