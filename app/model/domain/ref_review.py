from sqlalchemy import Column, Integer, String, DateTime,ForeignKey, Boolean
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship 


class RefReview(Base):
    __tablename__ = "tb_ref_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    reviewer = Column(String, nullable=False)
    reply = Column(String, nullable=True)
    is_replied = Column(Boolean, default=False)    
    platform_id = Column(Integer, ForeignKey("tb_ref_platforms.id"), nullable=False)
    platform = relationship("RefPlatform") 
    autoreply_id = Column(Integer, ForeignKey("tb_ref_autoreplies.id"), nullable=True)  # 자동응답 참조 추가
    autoreply = relationship("RefAutoReply", back_populates="reviews")  # 자동

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())