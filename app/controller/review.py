from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.model.schema.review import ReviewUpdate,ResponseReview, ReviewCreate
from app.crud.review import (get_reviews_by_store,get_reviews_by_store_names,
                             get_reviews as get_reviews_crud,
                             create_review as create_review_crud,
                            update_review as update_review_crud,    
                             delete_review as delete_review_crud,
                             get_reviews_by_platform,
                             get_reviews_all_platforms)
from app.crud.store import get_store_by_name,get_stores_all, get_stores_by_platform
from app.crud.platform import get_platform_by_name, get_platforms
from app.crud.user import get_user_by_email
from app.core.auth import verify_token

review_router = APIRouter()
security = HTTPBearer()

@review_router.get("/list/{platform}", response_model=list[ResponseReview])
def get_reviews(platform: str,
                offset: int = 0,
                limit: int = 10,
                credentials: HTTPAuthorizationCredentials = Depends(security),
                db: Session = Depends(get_db)):
    email = verify_token(credentials.credentials)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_user = get_user_by_email(db, email=email)
    
    # 플랫폼별 리뷰 조회
    if platform == "전체":
        reviews = get_reviews_all_platforms(db, limit=limit, offset=offset)
    else:
        reviews = get_reviews_by_platform(db, platform, limit=limit, offset=offset)
    
    res_reviews = []
    for review in reviews:
        res_review = ResponseReview(
            id=review.id,
            content=review.content,
            rating=review.rating,
            reviewer=review.reviewer,
            store=review.store.name,
            platform=review.platform.name,  # 플랫폼 정보 추가
            reply=review.reply,
            created_at=review.created_at.isoformat(),
            updated_at=review.updated_at.isoformat() if review.updated_at else None
        )
        res_reviews.append(res_review)
    return res_reviews

@review_router.post("/create", response_model=ResponseReview)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    # 플랫폼으로 스토어 찾기
    platform = get_platform_by_name(db, review.platform)
    if not platform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Platform not found"
        )
    
    # 해당 플랫폼의 기본 스토어 찾기 (첫 번째 스토어 사용)
    stores = get_stores_by_platform(db, platform.id)
    if not stores:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No store found for this platform"
        )
    
    store = stores[0]  # 첫 번째 스토어 사용
    
    db_review = create_review_crud(db, review, store_id=store.id, platform_id=platform.id)
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create review"
        )
    res_review = ResponseReview(
        id=db_review.id,
        content=db_review.content,
        rating=db_review.rating,
        reviewer=db_review.reviewer,
        store=store.name,
        platform=platform.name,
        reply=db_review.reply,
        created_at=db_review.created_at.isoformat(),
        updated_at=db_review.updated_at.isoformat() if db_review.updated_at else None
    )
    return res_review

@review_router.put("/update/{review_id}", response_model=ResponseReview)
def update_review(review_id: int, review: ReviewUpdate,
                  credentials: HTTPAuthorizationCredentials = Depends(security),
                  db: Session = Depends(get_db)):
    email = verify_token(credentials.credentials)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_review = update_review_crud(db, review_id, review)
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create review"
        )
    res_review = ResponseReview(
        id=db_review.id,
        content=db_review.content,
        rating=db_review.rating,
        reviewer=db_review.reviewer,
        store=db_review.store.name,
        platform=db_review.platform.name,  # 플랫폼 정보 추가
        reply=db_review.reply,
        created_at=db_review.created_at.isoformat(),
        updated_at=db_review.updated_at.isoformat() if db_review.updated_at else None
    )
    return res_review

@review_router.delete("/delete/{review_id}")
def delete_review(review_id: int,
                  credentials: HTTPAuthorizationCredentials = Depends(security),
                  db: Session = Depends(get_db)):
    email = verify_token(credentials.credentials)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_review = delete_review_crud(db, review_id)
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    return {"message": "Review deleted successfully"}