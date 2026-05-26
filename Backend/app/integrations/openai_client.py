from openai import OpenAI
from fastapi import status

from app.config import settings
from app.utils.exceptions import AppException


class OpenAIClient:
    def __init__(self, api_key: str | None = None):
        # Permite inyectar una API key en pruebas o usar la del archivo .env.
        self.api_key = api_key or settings.openai_api_key

        if not self.api_key:
            raise AppException(
                message="Falta configurar OPENAI_API_KEY en el archivo .env.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        self.client = OpenAI(api_key=self.api_key)

    def generate_sql_from_question(self, prompt: str) -> str:
        """
        Envía el prompt a OpenAI y devuelve únicamente el SQL generado.
        """

        try:
            response = self.client.responses.create(
                model=settings.openai_model,
                instructions=(
                    "Eres un experto en SQL Server. "
                    "Devuelve únicamente una consulta SQL SELECT válida. "
                    "No expliques nada y no uses markdown."
                ),
                input=prompt,
            )

            sql = response.output_text.strip()

            if not sql:
                raise AppException(
                    message="La IA no devolvió ninguna consulta SQL.",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return sql

        except AppException:
            raise

        except Exception as error:
            raise AppException(
                message=f"Error al consultar la IA: {error}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


