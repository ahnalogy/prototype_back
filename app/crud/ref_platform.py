from sqlalchemy.orm import Session
from app.model.domain.ref_platform import RefPlatform

def get_ref_platform_by_name(db: Session, platform: str):
   
    return db.query(RefPlatform).filter(RefPlatform.name == platform).first()