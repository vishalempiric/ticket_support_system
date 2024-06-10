from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EmailBase(BaseModel):
    thread_id: Optional[str]
    grant_id: Optional[str]
    e_id: Optional[str]
    subject: str
    body: str
    snippet: Optional[str]
    sender_name: str
    sender_email: str
    recipient_name: str
    recipient_email: str
    unread: Optional[bool] = False
    starred: Optional[bool] = False


class EmailCreate(EmailBase):
    pass


class EmailUpdate(EmailBase):
    pass


class EmailInDBBase(EmailBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Schema for response
class EmailResponse(EmailInDBBase):
    pass
