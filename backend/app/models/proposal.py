from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, timedelta
from app.database import Base

def _deadline_default():
    return datetime.utcnow() + timedelta(days=90)

class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    creator_name = Column(String(100), nullable=False)
    status = Column(String(20), default="activa")
    signature_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    deadline = Column(DateTime, default=_deadline_default)
    frozen_hash = Column(String(64), nullable=True)
