from fastapi import APIRouter

from app.utils.responses import success_response
from app.schemas.nql import NaturalQueryRequest, NaturalQueryResponse
from app.services.nql_service import nlq_service


router = APIRouter(prefix="/api/nql", tags=["nql"])


@router.post("/query", response_model=NaturalQueryResponse)
def query_natural_language(payload: NaturalQueryRequest) -> dict:
    # La ruta solo coordina entrada/salida HTTP; la logica queda en el servicio.
    result = nlq_service.process_question(payload)
    return success_response(
        "Consulta procesada correctamente",
        result.model_dump(),
    )