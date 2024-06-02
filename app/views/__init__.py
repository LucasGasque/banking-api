from fastapi import APIRouter
from .accounts import account_router
from .auth import auth_router
from .customer import customer_router
from .health import health_router
from .transfer_history import transfer_history_router


main_router = APIRouter(prefix="/api/v1")
main_router.include_router(account_router)
main_router.include_router(auth_router)
main_router.include_router(customer_router)
main_router.include_router(health_router)
main_router.include_router(transfer_history_router)
