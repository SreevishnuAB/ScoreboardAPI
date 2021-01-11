from pydantic import BaseModel, Field


class LoginResponse(BaseModel):
    authenticated: bool = Field(..., title="User authentication status")
    id: str = Field(..., title="User ID")
