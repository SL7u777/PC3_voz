from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class Signature(Base):
    __tablename__ = "signatures"

    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(Integer, ForeignKey("proposals.id"), nullable=False)
    citizen_name = Column(String(100), nullable=False)
    citizen_id = Column(String(20), nullable=False)
    signed_at = Column(DateTime, default=datetime.utcnow)
