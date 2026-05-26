from pydantic import BaseModel, Field, field_validator
from typing import Any
from app.utils.validators import ensure_question_is_not_empty

class NaturalQueryRequest(BaseModel):
    # Define el contrato de entrada del endpoint: una pregunta en lenguaje natural.
    question: str = Field(..., min_length=1, max_length=1000)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        # Reutiliza una validacion comun para rechazar textos vacios o con espacios.
        return ensure_question_is_not_empty(value)


class NaturalQueryData(BaseModel):
    # Modelo interno de la respuesta util: pregunta, SQL generado y filas resultantes.
    question: str
    generated_sql: str
    rows: list[dict[str, Any]]


class NaturalQueryResponse(BaseModel):
    # Estructura final uniforme que recibira el frontend.
    success: bool
    message: str
    data: NaturalQueryData