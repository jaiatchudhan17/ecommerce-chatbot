from fastapi import APIRouter

from genesis_ecommerce.api.v1 import orders, support

router = APIRouter(prefix="/v1")

# Include sub-routers
router.include_router(orders.router)
router.include_router(support.router)
