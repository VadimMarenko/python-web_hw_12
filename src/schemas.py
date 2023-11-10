from datetime import date

from pydantic import BaseModel, EmailStr, Field, condate


class UserModel(BaseModel):
    first_name: str = Field(default="", max_length=25)
    last_name: str = Field(default="", max_length=30)
    email: EmailStr | None
    phone_number: str = Field(default="", max_length=25)
    born_date: date | None
    description: str = Field(default="", max_length=250)


class ResponseUser(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None
    email: EmailStr | None
    phone_number: str | None
    born_date: date | None
    description: str | None

    class Config:
        from_attributes = True


class UserEmailModel(BaseModel):
    email: EmailStr
