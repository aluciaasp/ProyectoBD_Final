from typing import Any

from pydantic import BaseModel


class ApiResponse(BaseModel):
    # Esquema generico para documentar la forma comun de una respuesta JSON.
    success: bool
    message: str
    data: Any | None = None


    