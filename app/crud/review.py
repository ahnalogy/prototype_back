from sqlalchemy.orm import Session
from app.model.domain.review import Review
from app.model.domain.store import Store
from app.model.domain.platform import Platform
from app.model.schema.review import ReviewCreate, ReviewUpdate


def get_review(db: Session, review_id: int):
    return db.query(Review).filter(Review.id == review_id).first()

def get_reviews(db: Session, limit: int = 10, offset: int = 0):
    return db.query(Review).limit(limit).offset(offset).all()

def get_reviews_by_filters(db: Session,limit: int = 10, offset: int = 0, **filters,):
    query = db.query(Review)
    for key, value in filters.items():
        if hasattr(Review, key):
            query = query.filter(getattr(Review, key) == value)
    query = query.limit(limit).offset(offset)
    return query.all()

def get_reviews_by_store(db: Session, store_id: int,limit: int = 10, offset: int = 0):
    return db.query(Review).filter(Review.store_id == store_id).limit(limit).offset(offset).all()

def get_reviews_by_store_names(db: Session, store_names: list[str], limit: int = 10, offset: int = 0):
    return db.query(Review).join(Store).filter(Store.name.in_(store_names)).limit(limit).offset(offset).all()

# 플랫폼별 리뷰 조회 함수들 추가
def get_reviews_by_platform(db: Session, platform_name: str, limit: int = 10, offset: int = 0):
    return db.query(Review).join(Platform).filter(Platform.name == platform_name).limit(limit).offset(offset).all()

def get_reviews_all_platforms(db: Session, limit: int = 10, offset: int = 0):
    return db.query(Review).join(Platform).limit(limit).offset(offset).all()

def create_review(db: Session, review: ReviewCreate, store_id: int, platform_id: int = None):
    db_review = Review(
        content=review.content,
        rating=review.rating,
        reviewer=review.reviewer,  
        store_id=store_id,
        platform_id=platform_id or 1  # 기본값으로 플랫폼 ID 1 사용
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def update_review(db: Session, review_id: int, review_data: ReviewUpdate):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        return None
    for key, value in review_data.model_dump().items():
        setattr(db_review, key, value)
    db.commit()
    db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: int):
    review = db.query(Review).filter(Review.id == review_id).first()
    if review:
        db.delete(review)
        db.commit()
        return review
    return None