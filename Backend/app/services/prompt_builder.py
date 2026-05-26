from app.services.schema_context import SCHEMA_CONTEXT


def build_sql_prompt(question: str) -> str:
    """
    Construye el prompt que se enviará a Ollama.
    Incluye reglas de seguridad y contexto de la base DonaldV2.
    """

    return f"""
Eres un experto en SQL Server.
Tu tarea es convertir preguntas escritas en español a consultas SQL Server para la base de datos DonaldV2.

IMPORTANTE:
Debes devolver únicamente una consulta SQL.
No expliques nada.
No uses markdown.
No uses ```sql.
No uses LIMIT.
Usa sintaxis de SQL Server.
Usa TOP para limitar resultados.

REGLAS OBLIGATORIAS:
1. Solo puedes generar consultas SELECT.
2. No puedes generar INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, EXEC, CREATE, MERGE ni USE.
3. No inventes tablas.
4. No inventes columnas.
5. No agregues JOIN si la pregunta no lo necesita.
6. No agregues WHERE si el usuario no pidió un filtro específico.
7. Si el usuario pide mostrar registros de una tabla, usa SELECT TOP.
8. Si el usuario pide documentos fiscales, usa la tabla DocumentoFiscal.
9. No compares CodigoTipoDocumentoFiscal con texto como 'DF', porque CodigoTipoDocumentoFiscal es numérico.
10. Si la pregunta solicita eliminar, actualizar, insertar, crear o modificar datos, devuelve exactamente:
SELECT 'Consulta no permitida. Solo se permiten consultas de lectura.' AS Mensaje

EJEMPLOS OBLIGATORIOS:

Pregunta:
Muéstrame 10 documentos fiscales

Respuesta:
SELECT TOP 10 * FROM DocumentoFiscal

Pregunta:
Muestra documentos fiscales

Respuesta:
SELECT TOP 10 * FROM DocumentoFiscal

Pregunta:
Muéstrame 10 clientes

Respuesta:
SELECT TOP 10 * FROM Cliente

Pregunta:
Muéstrame 10 materiales

Respuesta:
SELECT TOP 10 * FROM Material

Pregunta:
¿Cuál es el total de ventas?

Respuesta:
SELECT SUM(ValorTotal) AS TotalVentas FROM DocumentoFiscal

CONTEXTO DE LA BASE DE DATOS:
{SCHEMA_CONTEXT}

PREGUNTA DEL USUARIO:
{question}

RESPUESTA SQL:
"""