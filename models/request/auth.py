from pydantic import BaseModel, Field, SecretStr, EmailStr

class User(BaseModel):
    id: str = Field(..., title="User ID")
    password: SecretStr = Field(..., title="Password")