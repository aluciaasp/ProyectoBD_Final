from app.database.connection import execute_select_query
from app.integrations.ollama_client import ollama_client
from app.schemas.nql import NaturalQueryData, NaturalQueryRequest
from app.services.prompt_builder import build_sql_prompt
from app.utils.sql_security import validate_select_only


class NaturalQueryService:
    def process_question(self, payload: NaturalQueryRequest) -> NaturalQueryData:
        """
        Flujo principal usando Ollama.

        Pasos:
        1. Construir un prompt con el contexto del esquema de DonaldV2.
        2. Pedir a Ollama una consulta SQL SELECT.
        3. Validar que el SQL generado sea solo lectura.
        4. Ejecutar la consulta en SQL Server.
        5. Devolver resultados al frontend.
        """

        # 1. Construir prompt con contexto de la base de datos.
        prompt = build_sql_prompt(payload.question)

        # 2. Generar SQL con Ollama.
        generated_sql = ollama_client.generate_sql_from_question(prompt)

        print("SQL GENERADO POR OLLAMA:")
        print(generated_sql)

        safe_sql = validate_select_only(generated_sql)

        print("SQL VALIDADO:")
        print(safe_sql)

        rows = execute_select_query(safe_sql)

        # 5. Devolver respuesta.
        return NaturalQueryData(
            question=payload.question,
            generated_sql=safe_sql,
            rows=rows,
        )


# Instancia reutilizable para no crear el servicio en cada request.
nlq_service = NaturalQueryService()