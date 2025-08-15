from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.model.domain.platform import Platform
from app.model.schema.platform import PlatformCreate, ResponsePlatform
from app.crud.platform import delete_platform as delete_platform_crud
from app.crud.ref_review import get_ref_reviews_by_platform
from app.crud.ref_platform import get_ref_platform_by_name
from app.crud.review import create_review as create_review_crud
from app.model.schema.review import ReviewCreate
from app.crud.review import get_review_by_created_atN_platform
from app.crud.ref_review import get_ref_reviews_by_created_at

platform_router = APIRouter()

#get: 데이터를 가져오는거
#post: 데이터를 생성하는거 
#put: 데이터를 수정하는거
#delete: 데이터를 삭제하는거

 # @: decorator
 # 플랫폼 등록하기
@platform_router.post("/create")
def create_platform(platform_crate: PlatformCreate, db: Session = Depends(get_db)):
    try:
        print("platform_crate:", platform_crate)
        # 플랫폼 중복 체크
        existing_platform = db.query(Platform).filter(Platform.name == platform_crate.name).first()
        if existing_platform:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 등록된 플랫폼입니다."
            )

        platform = Platform(
            name=platform_crate.name
        )
        db.add(platform)
        db.commit()
        db.refresh(platform)

        latest_review = get_review_by_created_atN_platform(db, platform.id)
        if latest_review:
            late_ref_reviews = get_ref_reviews_by_created_at(db, latest_review.created_at, platform.id)
            for ref_review in late_ref_reviews:
                review_data = ReviewCreate(
                    content=ref_review.content,
                    rating=ref_review.rating,
                    reviewer=ref_review.reviewer,
                    platform=ref_review.platform  # platform 이름이 ref_review에 있다고 가정
                )
                create_review_crud(db, review_data, platform_id=platform.id, autoreply_id=ref_review.autoreply_id)
        else:
            ref_platform = get_ref_platform_by_name(db, platform.name)
            ref_reviews = get_ref_reviews_by_platform(db, ref_platform.id, limit=10)
            for ref_review in ref_reviews:
                review_data = ReviewCreate(
                    content=ref_review.content,
                    rating=ref_review.rating,
                    reviewer=ref_review.reviewer,
                    platform=ref_platform.name
                )
                create_review_crud(db, review_data, platform_id=platform.id, autoreply_id=ref_review.autoreply_id)

        return {"name": platform.name}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"플랫폼 생성 중 오류가 발생했습니다: {str(e)}"
        )

@platform_router.get("/list", response_model=list[ResponsePlatform])
def get_platforms(db: Session = Depends(get_db)):
    platforms = db.query(Platform).all()

    results = []
    if platforms:

        for platform in platforms:
            result = ResponsePlatform(
                id=platform.id,
                name=platform.name
            )
            results.append(result)
    return results
  

@platform_router.delete("/delete/{platform_id}") # platform의 이름을 받아서 삭제
def delete_platform(platform_id: int, db: Session = Depends(get_db)):
    platform = delete_platform_crud(db, platform_id)
    if not platform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Platform not found"
        )
   
    return{"name": platform.name}