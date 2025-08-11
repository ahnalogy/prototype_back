from pydantic import BaseModel
from typing import Optional

class ReviewBase(BaseModel):
    content: str
    rating: int
    reviewer: str

class ReviewCreate(ReviewBase):
    platform: str 

class ReviewUpdate(BaseModel):
    content: Optional[str] = None
    rating: Optional[int] = None
    reviewer: Optional[str] = None
    reply: Optional[str] = None
    is_replied: Optional[bool] = False

class ResponseReview(ReviewBase):
    id: int
    store: str
    platform: str  # 플랫폼 정보 추가
    reply: Optional[str] = None
    is_replied: Optional[bool] = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True  # Pydantic V2 호환