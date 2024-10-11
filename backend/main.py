from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError

from auth.views import auth_router
from exc_handlers.base import value_error_handler, related_errors_handler
from views.referrals import referral_router

app = FastAPI(title="Test referral app")

exc_handlers = {
    ValueError: value_error_handler,
    IntegrityError: related_errors_handler,
}
routers = {
    "/auth": auth_router,
    "/referrals": referral_router,
}

for exception, handler in exc_handlers.items():
    app.add_exception_handler(exception, handler)

for prefix, router in routers.items():
    app.include_router(router, prefix=prefix)
