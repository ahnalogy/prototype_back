from sqlalchemy import Column, Integer, String, DateTime,ForeignKey, Boolean
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship 


class RefAutoReply(Base):
    __tablename__ = "tb_ref_autoreplies"
    
    id = Column(Integer, primary_key=True, index=True)
    casual = Column(String, nullable=False)
    biz_casual = Column(String, nullable=False)
    formal = Column(String, nullable=False)
    
    casual_en = Column(String, nullable=False)
    biz_casual_en = Column(String, nullable=False)
    formal_en = Column(String, nullable=False)

    ref_reviews = relationship("RefReview", back_populates="autoreply")  # ref리뷰와의 관계 설정
    reviews = relationship("Review", back_populates="autoreply")  # 리뷰와의 관계 설정
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())