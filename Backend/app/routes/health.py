from fastapi import APIRouter

from app.utils.responses import success_response


router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict:
    return success_response("API funcionando correctamente")