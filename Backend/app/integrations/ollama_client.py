import requests
from fastapi import status

from app.config import settings
from app.utils.exceptions import AppException


class OllamaClient:
    def __init__(self):
        self.base_url = settings.ollama_base_url.rstrip("/")
        self.model = settings.ollama_model

    def generate_sql_from_question(self, prompt: str) -> str:
        """
        Envía el prompt a Ollama y devuelve únicamente el SQL generado.
        """

        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0
            }
        }

        try:
            response = requests.post(url, json=payload, timeout=120)

            if response.status_code != 200:
                raise AppException(
                    message=f"Error al consultar Ollama: {response.text}",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            data = response.json()
            sql = data.get("response", "").strip()

            if not sql:
                raise AppException(
                    message="Ollama no devolvió ninguna consulta SQL.",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return sql

        except requests.exceptions.ConnectionError:
            raise AppException(
                message=(
                    "No se pudo conectar con Ollama. "
                    "Verifica que Ollama esté instalado y ejecutándose."
                ),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except requests.exceptions.Timeout:
            raise AppException(
                message="Ollama tardó demasiado en responder.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


ollama_client = OllamaClient()