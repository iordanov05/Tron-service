from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.db.session import Base

class TronRequest(Base):
    __tablename__ = "tron_requests"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True, nullable=False)
    balance = Column(Float, nullable=False)
    bandwidth = Column(Integer, nullable=False)
    energy = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
