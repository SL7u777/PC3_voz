from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from app.database import Base

class Modification(Base):
    __tablename__ = "modifications"

    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(Integer, ForeignKey("proposals.id"), nullable=False)
    author_name = Column(String(100), nullable=False)
    section = Column(String(100), nullable=False)
    proposed_change = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
