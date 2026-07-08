from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


async def http_exception_handler(
    _request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    """HTTP 예외를 JSend 스타일 응답으로 변환한다."""
    if exc.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "message": str(exc.detail),
            },
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "fail",
            "data": {
                "detail": exc.detail,
            },
        },
    )


async def validation_exception_handler(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """요청 검증 예외를 JSend fail 응답으로 변환한다."""
    return JSONResponse(
        status_code=422,
        content={
            "status": "fail",
            "data": {
                "detail": exc.errors(),
            },
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """FastAPI 애플리케이션에 공통 예외 핸들러를 등록한다."""
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
