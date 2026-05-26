from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.utils.responses import error_response


class AppException(Exception):
    # Excepcion propia para errores controlados de la aplicacion.
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    # Convierte errores controlados en una respuesta JSON uniforme.
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.message),
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    # Simplifica los errores de Pydantic para que el frontend reciba mensajes claros.
    details = [
        {
            "field": ".".join(str(part) for part in error.get("loc", [])),
            "message": error.get("msg", "Valor invalido"),
        }
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_response(
            "La solicitud contiene datos invalidos",
            jsonable_encoder(details),
        ),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # Evita exponer detalles internos cuando ocurre un error no esperado.
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response("Ocurrio un error interno en el servidor"),
    )