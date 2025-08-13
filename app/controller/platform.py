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
from app.crud.review import get_review_by_created_at
from app.crud.ref_review import get_ref_reviews_by_created_at

platform_router = APIRouter()

#get: 데이터를 가져오는거
#post: 데이터를 생성하는거 
#put: 데이터를 수정하는거
#delete: 데이터를 삭제하는거

 # @: decorator
 # 플랫폼 등록하기
@platform_router.post("/create") # input으로 값을 받아오는거면 post라고 생각하는게 좋음
def create_platform(platform_crate: PlatformCreate, db: Session = Depends(get_db)):
    print("platform_crate:", platform_crate)
    platform = Platform(
        name=platform_crate.name #platform tb에 name 컬럼에 값을 넣어줌
        
    )
    db.add(platform) #platform 객체 -> db에 추가(column)
    db.commit() # db에 반영
    db.refresh(platform) # db -> platform 객체를 새로 불러옴

    # ref_review에서 해당 플랫폼의 리뷰를 가져와서 review 테이블에 저장하기
    latest_review=get_review_by_created_at(db) # 최신 리뷰를 가져옴
    if latest_review:
        late_ref_reviews=get_ref_reviews_by_created_at(db, latest_review.created_at, platform.id) # 최신 리뷰 이후의 리뷰를 가져옴
        # db에 저장 
        for ref_review in late_ref_reviews:
            review_data = ReviewCreate(
                content=ref_review.content,
                rating=ref_review.rating,
                reviewer=ref_review.reviewer,
                platform=ref_platform.name
            )
            create_review_crud(db, review_data,platform_id=platform.id, autoreply_id=ref_review.autoreply_id)
    else:
        ref_platform=get_ref_platform_by_name(db, platform.name) # 플랫폼 이름으로 ref_platform에서 해당 플랫폼을 가져옴
        ref_reviews=get_ref_reviews_by_platform(db, ref_platform.id, limit=10) # 리뷰를 가져오는 함수 호출
        for ref_review in ref_reviews:
            review_data = ReviewCreate(
                content=ref_review.content,
                rating=ref_review.rating,
                reviewer=ref_review.reviewer,
                platform=ref_platform.name
            )
            create_review_crud(db, review_data,platform_id=platform.id, autoreply_id=ref_review.autoreply_id)

    return{"name": platform.name}

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