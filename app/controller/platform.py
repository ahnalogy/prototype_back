from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.model.domain.platform import Platform
from app.model.schema.platform import PlatformCreate

platform_router = APIRouter()

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

@platform_router.get("/list", response_model=list[PlatformCreate])
def get_platforms(db: Session = Depends(get_db)):
    platforms = db.query(Platform).all()
    if not platforms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No platforms found"
        )
    return platforms