from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator, field_validator

TEL_MOBILE_RULE = r"(\+)[1-9][0-9]{10}"
TEL_HOME_RULE = r"[0-9]{6}"


class ContactSchema(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    tel_mobile: str = Field(..., pattern=TEL_MOBILE_RULE)
    tel_home: str = Field(pattern=TEL_HOME_RULE)

    class Config:
        schema_extra = {
            "username": "John Doe",
            "email": "john@mail.com",
            "tel_mobile": "+70001112233",
            "tel_home": "332211"
        }


class UpdateContactModel(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    tel_mobile: Optional[str] = None
    tel_home: Optional[str] = None


def ResponseModel(data, message):
    return {"data": [data], "code": 200, "message": message}


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}