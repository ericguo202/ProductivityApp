from pydantic import BaseModel, EmailStr

class EmailIn(BaseModel):
    sender: EmailStr
    subject: str | None
    body: str 
