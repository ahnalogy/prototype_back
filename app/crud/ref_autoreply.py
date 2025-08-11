from sqlalchemy.orm import Session
from app.model.domain.ref_autoreply import RefAutoReply

def create_ref_autoreply(db: Session, casual: str, biz_casual: str, formal: str,
                         casual_en: str, biz_casual_en: str, formal_en: str):
    new_autoreply = RefAutoReply(
        casual=casual,
        biz_casual=biz_casual,
        formal=formal,
        casual_en=casual_en,
        biz_casual_en=biz_casual_en,
        formal_en=formal_en
    )
    
    db.add(new_autoreply)
    db.commit()
    db.refresh(new_autoreply)
    
    return new_autoreply

