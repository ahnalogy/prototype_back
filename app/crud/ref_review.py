from sqlalchemy.orm import Session
from app.model.domain.ref_review import RefReview

def get_ref_reviews_by_platform(db: Session, platform_id: int, limit: int = 10, offset: int = 0):
    return db.query(RefReview).filter(RefReview.platform_id == platform_id).limit(limit).offset(offset).all()

