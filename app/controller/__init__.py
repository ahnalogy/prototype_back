from fastapi import APIRouter
from app.controller.user import user_router
from app.controller.store import store_router
from app.controller.review import review_router
from app.controller.recommend import recommend_router
from app.controller.autoreview import autoreview_router
from app.controller.translate import trans_router
from app.controller.platform import platform_router
from app.controller.ref_platform import ref_platform_router
from app.controller.ref_review import ref_review_router

router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(store_router, prefix="/store", tags=["store"])
router.include_router(review_router, prefix="/review", tags=["review"])
router.include_router(recommend_router, prefix="/recommend", tags=["recommend"])
router.include_router(autoreview_router, prefix="/autoreview", tags=["autoreview"])
router.include_router(trans_router, prefix="/translate", tags=["translate"])
router.include_router(platform_router, prefix="/platform", tags=["platform"]) # platform 로 시작하고, platform_router 속해 있으면 platform.py에 있는 함수들을 가져올 때 prefix=""내용을 붙이고 시작.
router.include_router(ref_platform_router, prefix="/refplatform", tags=["refplatform"])
router.include_router(ref_review_router, prefix="/refreview", tags=["refreview"])
