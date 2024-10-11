from re import search

from fastapi.responses import JSONResponse


async def value_error_handler(request, exc):
    details = str(exc.args) if exc.args else str(exc)
    return JSONResponse(status_code=400, content={"detail": details})


async def related_errors_handler(request, exc):
    details = (
        search(r"DETAIL:\s*(.*)", str(exc.orig)).group(1)
        if getattr(exc, "orig")
        else str(exc)
    )
    return JSONResponse(status_code=400, content={"detail": details})
