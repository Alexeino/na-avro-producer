from fastapi import APIRouter
from .orders.views import order_router

router = APIRouter()
router.include_router(order_router,prefix="/orders",tags=["orders",])

@router.get("/")
async def health():
    return "Ok"