from sqlalchemy import Column, Integer, String, DateTime,ForeignKey, Boolean
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship  # 추가


class Platform(Base):
    __tablename__ = "tb_platforms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())