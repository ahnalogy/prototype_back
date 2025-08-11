from pydantic import BaseModel
from typing import Optional
from app.model.schema.autoreview import AutoReviewResponse

class RefReviewBase(BaseModel):
    content: str
    rating: int
    reviewer: str

class RefReviewCreate(RefReviewBase):
    platform: str 

class RefReviewUpdate(BaseModel):
    content: Optional[str] = None
    rating: Optional[int] = None
    reviewer: Optional[str] = None
    reply: Optional[str] = None
    is_replied: Optional[bool] = False

class RefResponseReview(RefReviewBase):
    id: int
    content: Optional[str] = None
    autoreply: AutoReviewResponse
    platform_id: int  # 플랫폼 정보 추가
    reply: Optional[str] = None
    is_replied: Optional[bool] = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True  # Pydantic V2 호환