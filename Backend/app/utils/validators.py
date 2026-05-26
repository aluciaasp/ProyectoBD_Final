FORBIDDEN_SQL_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "TRUNCATE",
    "ALTER",
    "CREATE",
    "EXEC",
    "EXECUTE",
    "MERGE",
}


def ensure_question_is_not_empty(question: str) -> str:
    """
    Valida que la pregunta no venga vacía.
    Devuelve la pregunta limpia.
    """

    if question is None:
        raise ValueError("Por favor ingrese una pregunta")

    cleaned_question = question.strip()

    if not cleaned_question:
        raise ValueError("Por favor ingrese una pregunta")

    return cleaned_question


def is_read_only_sql(sql: str) -> bool:
    """
    Valida que una consulta sea únicamente de lectura.
    """

    normalized_sql = sql.upper().strip()

    if not normalized_sql.startswith("SELECT"):
        return False

    tokens = {token.strip(";,()") for token in normalized_sql.split()}

    return FORBIDDEN_SQL_KEYWORDS.isdisjoint(tokens)