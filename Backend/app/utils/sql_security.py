import re

from fastapi import status

from app.utils.exceptions import AppException


FORBIDDEN_WORDS = [
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "truncate",
    "create",
    "merge",
    "exec",
    "execute",
    "grant",
    "revoke",
    "backup",
    "restore",
    "use",
    "into",
]


def clean_sql(sql: str) -> str:
    """
    Limpia la respuesta de la IA si viene con formato markdown.
    Ejemplo:
    ```sql
    SELECT * FROM Cliente
    ```
    """
    sql = sql.strip()

    sql = re.sub(r"^```sql", "", sql, flags=re.IGNORECASE).strip()
    sql = re.sub(r"^```", "", sql).strip()
    sql = re.sub(r"```$", "", sql).strip()

    return sql


def validate_select_only(sql: str) -> str:
    """
    Valida que la consulta generada por la IA sea únicamente SELECT.
    Bloquea instrucciones peligrosas como DELETE, DROP, UPDATE e INSERT.
    """
    sql = clean_sql(sql)

    if not sql:
        raise AppException(
            "La IA no generó ninguna consulta SQL.",
            status.HTTP_400_BAD_REQUEST,
        )

    normalized = sql.lower().strip()

    if not normalized.startswith("select"):
        raise AppException(
            "Consulta no permitida. Solo se permiten consultas SELECT.",
            status.HTTP_400_BAD_REQUEST,
        )

    if "--" in normalized or "/*" in normalized or "*/" in normalized:
        raise AppException(
            "Consulta no permitida. No se permiten comentarios SQL.",
            status.HTTP_400_BAD_REQUEST,
        )

    if ";" in normalized.rstrip(";"):
        raise AppException(
            "Consulta no permitida. Solo se permite una instrucción SQL.",
            status.HTTP_400_BAD_REQUEST,
        )

    for word in FORBIDDEN_WORDS:
        pattern = rf"\b{word}\b"
        if re.search(pattern, normalized):
            raise AppException(
                f"Consulta no permitida. Se detectó la palabra prohibida: {word.upper()}",
                status.HTTP_400_BAD_REQUEST,
            )

    return sql.rstrip(";")