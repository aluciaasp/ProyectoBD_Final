from typing import Any
from app.database.connection import get_connection
from app.utils.validators import is_read_only_sql

def execute_read_only_query(sql: str) -> list[dict[str, Any]]:
    if not is_read_only_sql(sql):
        raise ValueError("Solo se permiten consultas de solo lectura")
    
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

def execute_write_query(sql: str) -> None:
    if is_read_only_sql(sql):
        raise ValueError("Solo se permiten consultas de escritura")
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        
        columns = [column[0] for column in cursor.description]
        return[dict[str, Any] (zip[tuple[Any, Any]](columns, row)) for row in cursor.fetchall()]
        
