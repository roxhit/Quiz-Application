from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import List, Optional
import re


class UserRegistration(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

    @field_validator("password")
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v


class UserLogin(BaseModel):
    email: str
    password: str


class AdminRegistration(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

    @field_validator("password")
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v


class AdminLogin(BaseModel):
    email: str
    password: str
