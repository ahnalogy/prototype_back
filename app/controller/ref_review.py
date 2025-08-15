from fastapi import APIRouter, Depends, HTTPException, status
from app.model.schema.ref_review import RefReviewCreate, RefResponseReview
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.model.domain.ref_review import RefReview
from app.service.auto_review import generate_review_response, translate_ko2en
from app.utils.check import check_language
from app.crud.ref_autoreply import create_ref_autoreply
from app.model.schema.autoreview import AutoReviewResponse
from app.crud.ref_platform import get_ref_platform_by_name
from app.crud.review import create_review as create_review_crud
from app.model.schema.review import ReviewCreate
from app.crud.platform import get_platform_by_name

ref_review_router = APIRouter()

@ref_review_router.post("/create", response_model=RefResponseReview)
def create_ref_review(ref_review: RefReviewCreate, db: Session = Depends(get_db)):
    

    # 한글 응답 생성
    casual_text = generate_review_response(ref_review.content,ref_review.rating, tone="친근한", language="ko")
    formal_text = generate_review_response(ref_review.content,ref_review.rating, tone="정중한", language="ko")
    business_text = generate_review_response(ref_review.content,ref_review.rating, tone="공손한", language="ko")

    # 영어 응답 생성
    casual_en_text = translate_ko2en(casual_text)
    formal_en_text = translate_ko2en(formal_text)
    business_en_text = translate_ko2en(business_text)

    # 자동응답 생성
    auto_reply = create_ref_autoreply(
        db,
        casual=casual_text,
        biz_casual=business_text,
        formal=formal_text,
        casual_en=casual_en_text,
        biz_casual_en=business_en_text,
        formal_en=formal_en_text
    )
    if auto_reply is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create auto reply"
        )


    # 플랫폼 정보 확인
    ref_platform = get_ref_platform_by_name(db, ref_review.platform)
    if not ref_platform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Platform not found"
        )
    
    # Create a new reference review
    new_ref_review = RefReview(
        content=ref_review.content,
        rating=ref_review.rating,
        reviewer=ref_review.reviewer,
        reply=None,
        is_replied=False,
        platform_id=ref_platform.id,
        autoreply_id=auto_reply.id  # Optional autoreply reference
    )
    
    db.add(new_ref_review)
    db.commit()
    db.refresh(new_ref_review)

    res_auto_reply=AutoReviewResponse(
        casual=auto_reply.casual,
        biz_casual=auto_reply.biz_casual,
        formal=auto_reply.formal,
        casual_en=auto_reply.casual_en,
        biz_casual_en=auto_reply.biz_casual_en,
        formal_en=auto_reply.formal_en
    )
    
    platform = get_platform_by_name(db,ref_review.platform)  # Ensure platform exists
    if platform:
        review_data = ReviewCreate(
            content=ref_review.content,
            rating=ref_review.rating,
            reviewer=ref_review.reviewer,
            platform=platform.name
        )
        create_review_crud(db, review_data, platform_id=platform.id, autoreply_id=auto_reply.id)

    res_review = RefResponseReview(
        id=new_ref_review.id,
        content=new_ref_review.content,
        rating=new_ref_review.rating,
        reviewer=new_ref_review.reviewer,
        reply=None,  # Initial reply is None
        is_replied=new_ref_review.is_replied,
        platform_id=new_ref_review.platform_id,
        autoreply=res_auto_reply  # Include the auto reply in the response
    )
    return res_review