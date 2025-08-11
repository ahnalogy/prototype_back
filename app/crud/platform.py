from sqlalchemy.orm import Session
from app.model.domain.platform import Platform
from app.model.schema.platform import PlatformCreate, PlatformUpdate

def get_platform(db: Session, platform_id: int):
    return db.query(Platform).filter(Platform.id == platform_id).first()

def get_platform_by_name(db: Session, name: str):
    return db.query(Platform).filter(Platform.name == name).first()

def get_platforms(db: Session, limit: int = 100, offset: int = 0):
    return db.query(Platform).limit(limit).offset(offset).all()

def create_platform(db: Session, platform: PlatformCreate):
    db_platform = Platform(name=platform.name)
    db.add(db_platform)
    db.commit()
    db.refresh(db_platform)
    return db_platform

def update_platform(db: Session, platform_id: int, platform_data: PlatformUpdate):
    db_platform = db.query(Platform).filter(Platform.id == platform_id).first()
    if not db_platform:
        return None
    for key, value in platform_data.model_dump().items():
        if value is not None:
            setattr(db_platform, key, value)
    db.commit()
    db.refresh(db_platform)
    return db_platform

def delete_platform(db: Session, platform_id: int):
    platform = db.query(Platform).filter(Platform.id == platform_id).first()
    if platform:
        db.delete(platform)
        db.commit()
        return platform
    return None
