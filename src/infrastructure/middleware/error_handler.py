"""Middleware de manejo de errores global."""

import logging
from typing import Callable, Awaitable, Any

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp

logger: logging.Logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware que captura excepciones y devuelve respuestas JSON estructuradas."""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Procesa la solicitud y captura excepciones."""
        try:
            response: Response = await call_next(request)
            return response
        except ValueError as exc:
            logger.warning(f"ValueError en {request.url.path}: {str(exc)}")
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": str(exc),
                    "path": str(request.url.path),
                    "error_type": "validation_error"
                }
            )
        except Exception as exc:
            logger.error(
                f"Error no manejado en {request.url.path}: {str(exc)}",
                exc_info=True
            )
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "message": "Error interno del servidor",
                    "path": str(request.url.path),
                    "error_type": "internal_error"
                }
            )
