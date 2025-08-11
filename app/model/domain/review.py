from sqlalchemy import Column, Integer, String, DateTime,ForeignKey, Boolean
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship  # 추가


class Review(Base):
    __tablename__ = "tb_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    reviewer = Column(String, nullable=False)
    reply = Column(String, nullable=True)
    is_replied = Column(Boolean, default=False)    
    store_id = Column(Integer, ForeignKey("tb_store.id"), nullable=False)
    platform_id = Column(Integer, ForeignKey("tb_platforms.id"), nullable=False)  # 플랫폼 정보 추가

    store = relationship("Store", back_populates="review")
    platform = relationship("Platform")  # 플랫폼 관계 추가

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())