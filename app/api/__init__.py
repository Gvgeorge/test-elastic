from fastapi import APIRouter
from .posts import router as posts_router
from .reports import router as reports_router
from .rubrics import router as rubrics_router
from .elastic import router as elastic_router


router = APIRouter()
router.include_router(posts_router)
router.include_router(reports_router)
router.include_router(rubrics_router)
router.include_router(elastic_router)
