from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.model.domain.platform import Platform
from app.model.schema.platform import PlatformCreate, ResponsePlatform
from app.crud.platform import delete_platform as delete_platform_crud

platform_router = APIRouter()

#get: 데이터를 가져오는거
#post: 데이터를 생성하는거 
#put: 데이터를 수정하는거
#delete: 데이터를 삭제하는거

 # @: decorator
@platform_router.post("/create") # input으로 값을 받아오는거면 post라고 생각하는게 좋음
def create_platform(platform_crate: PlatformCreate, db: Session = Depends(get_db)):

    platform = Platform(
        name=platform_crate.name #platform tb에 name 컬럼에 값을 넣어줌
        
    )
    db.add(platform) #platform 객체 -> db에 추가(column)
    db.commit() # db에 반영
    db.refresh(platform) # db -> platform 객체를 새로 불러옴
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