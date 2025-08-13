from sqlalchemy.orm import Session
from app.model.domain.ref_review import RefReview
from datetime import datetime

def get_ref_reviews_by_platform(db: Session, platform_id: int, limit: int = 10, offset: int = 0):
    return db.query(RefReview).filter(RefReview.platform_id == platform_id).limit(limit).offset(offset).all()

def get_ref_reviews_by_created_at(db: Session, created_at: datetime, platform_id: int):
    return db.query(RefReview).filter(RefReview.created_at > created_at, RefReview.platform_id == platform_id).all()