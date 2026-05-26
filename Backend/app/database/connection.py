from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pyodbc
from fastapi import status

from app.config import settings
from app.utils.exceptions import AppException


def build_connection_string() -> str:
    """
    Construye la cadena de conexión a SQL Server.
    Permite usar Windows Authentication o usuario/contraseña SQL Server.
    """
    if settings.db_trusted_connection.lower() == "yes":
        return (
            f"DRIVER={{{settings.db_driver}}};"
            f"SERVER={settings.db_server};"
            f"DATABASE={settings.db_database};"
            "Trusted_Connection=yes;"
            "Encrypt=no;"
            "TrustServerCertificate=yes;"
        )

    return (
        f"DRIVER={{{settings.db_driver}}};"
        f"SERVER={settings.db_server};"
        f"DATABASE={settings.db_database};"
        f"UID={settings.db_user};"
        f"PWD={settings.db_password};"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    )


def get_connection() -> pyodbc.Connection:
    """
    Crea la conexión con SQL Server.
    """
    try:
        return pyodbc.connect(build_connection_string(), timeout=10)

    except Exception as error:
        raise AppException(
            message=f"No se pudo conectar a SQL Server: {error}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def convert_value(value: Any):
    """
    Convierte valores de SQL Server a formatos compatibles con JSON.
    """
    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    return value


def execute_select_query(sql: str) -> list[dict]:
    """
    Ejecuta una consulta SELECT y devuelve los resultados como lista de diccionarios.
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(sql)

            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()

            results = []

            for row in rows:
                item = {}
                for column_name, value in zip(columns, row):
                    item[column_name] = convert_value(value)

                results.append(item)

            return results

    except AppException:
        raise

    except Exception as error:
        raise AppException(
            message=f"Error al ejecutar la consulta SQL: {error}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )