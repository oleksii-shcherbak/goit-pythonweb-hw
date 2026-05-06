from datetime import date

from pydantic import BaseModel, EmailStr, Field


class ContactBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100, examples=["John"])
    last_name: str = Field(..., min_length=1, max_length=100, examples=["Doe"])
    email: EmailStr = Field(..., examples=["john.doe@example.com"])
    phone: str = Field(..., min_length=3, max_length=20, examples=["+380501234567"])
    birthday: date = Field(..., examples=["1990-06-15"])
    extra_info: str | None = Field(default=None, examples=["Friend from university"])


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, min_length=3, max_length=20)
    birthday: date | None = None
    extra_info: str | None = None


class ContactResponse(ContactBase):
    id: int

    model_config = {"from_attributes": True}
