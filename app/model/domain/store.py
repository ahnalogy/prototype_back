from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship  
from app.core.database import Base

class Store(Base):
    __tablename__ = "tb_store"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    business_number = Column(Integer, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("tb_user.id"), nullable=False)
    user = relationship("User", back_populates="stores")  # 추가
    platform_id = Column(Integer, ForeignKey("tb_platforms.id"), nullable=False)
    platform = relationship("Platform", back_populates="store")  # 추가
    review = relationship("Review", back_populates="store", cascade="all, delete-orphan")  # 추가

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())