from pydantic import BaseModel, EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr

class ForgotPasswordVerify(BaseModel):
    token: str
    new_password: str
    
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
