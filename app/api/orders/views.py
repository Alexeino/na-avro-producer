from fastapi import APIRouter
from app.core.settings import settings
from .schemas import OrderSchema

order_router = APIRouter()


@order_router.post("/create")
async def order_create(order:OrderSchema):
    return order.model_dump()

