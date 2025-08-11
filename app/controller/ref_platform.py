from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.model.domain.ref_platform import RefPlatform
from app.model.schema.platform import ResponsePlatform

ref_platform_router = APIRouter()


@ref_platform_router.get("/list", response_model=list[ResponsePlatform])
def get_platforms(db: Session = Depends(get_db)):
    platforms = db.query(RefPlatform).all()

    results = []
    if platforms:

        for platform in platforms:
            result = ResponsePlatform(
                id=platform.id,
                name=platform.name
            )
            results.append(result)
    return results

