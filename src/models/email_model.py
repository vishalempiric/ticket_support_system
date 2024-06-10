from src.config import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    thread_model_id = Column(Integer, ForeignKey('threads.id'))
    thread_id = Column(String)
    grant_id = Column(String)
    e_id = Column(String)
    subject = Column(String)
    body = Column(Text)
    snippet = Column(String)
    sender_name = Column(String)
    sender_email = Column(String)   
    recipient_name = Column(String)
    recipient_email = Column(String)
    unread = Column(Boolean, default=False)
    starred = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())








