from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import health, nql
from app.utils.exceptions import (
    AppException,
    app_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)


# Punto de entrada principal de FastAPI.
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API para consultas en lenguaje natural sobre DonaldV2.",
)

# CORS permite que el frontend local pueda llamar al backend desde el navegador.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manejadores de errores.
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# Registro de rutas.
app.include_router(health.router)
app.include_router(nql.router)