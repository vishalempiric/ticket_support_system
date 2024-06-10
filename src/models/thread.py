from src.config import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Thread(Base):
    __tablename__ = 'threads'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    thread_id = Column(String)
    status = Column(String)
    priority = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

