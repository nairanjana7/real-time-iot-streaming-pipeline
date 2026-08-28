from pydantic import BaseModel, EmailStr


class CompanyRegisterRequest(BaseModel):
    company_name: str
    industry: str
    admin_name: str
    admin_email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
