from app.database.connection import execute_select_query
from app.integrations.ollama_client import ollama_client
from app.schemas.nql import NaturalQueryData, NaturalQueryRequest
from app.services.prompt_builder import build_sql_prompt
from app.utils.sql_security import validate_select_only


def limpiar_texto_sql(texto: str) -> str:
    """
    Evita romper el SQL si el texto trae comillas simples.
    """
    return texto.replace("'", "''").strip()


def obtener_nombre_sucursal(question: str) -> str | None:
    """
    Extrae el nombre de la sucursal desde la pregunta.

    Ejemplo:
    - "Cuál fue el total de ventas en el último trimestre en la Sucursal Jalapa"
      devuelve "Sucursal Jalapa"

    - "Cuál fue el total de ventas en el último trimestre en la Sucursal Jutiapa"
      devuelve "Sucursal Jutiapa"
    """
    pregunta = question.strip()
    pregunta_lower = pregunta.lower()

    if "sucursal" not in pregunta_lower:
        return None

    partes = pregunta.split("Sucursal", 1)

    if len(partes) < 2:
        partes = pregunta_lower.split("sucursal", 1)

    if len(partes) < 2:
        return None

    nombre = partes[1].strip()
    nombre = nombre.replace("?", "").replace("¿", "").strip()
    nombre = nombre.rstrip(".,;:")

    if not nombre:
        return None

    if nombre.lower().startswith("sucursal"):
        return nombre.title()

    return f"Sucursal {nombre.title()}"


def get_predefined_sql(question: str) -> str | None:
    """
    Devuelve SQL corregido para preguntas avanzadas conocidas.

    Esto ayuda cuando la IA genera columnas incorrectas o sintaxis de otro motor,
    por ejemplo LIMIT de MySQL o columnas que no existen.
    """
    normalized_question = question.lower().strip()

    # Seguridad: si el usuario intenta modificar datos, devolver SELECT seguro.
    acciones_prohibidas = [
        "elimina",
        "eliminar",
        "borra",
        "borrar",
        "actualiza",
        "actualizar",
        "inserta",
        "insertar",
        "crea",
        "crear",
        "modifica",
        "modificar",
        "drop",
        "delete",
        "update",
        "insert",
    ]

    if any(accion in normalized_question for accion in acciones_prohibidas):
        return "SELECT 'Consulta no permitida. Solo se permiten consultas de lectura.' AS Mensaje"

    # Consulta avanzada: ventas por sucursal en último trimestre.
    pregunta_ventas_sucursal = (
        "total de ventas" in normalized_question
        and "sucursal" in normalized_question
        and (
            "último trimestre" in normalized_question
            or "ultimo trimestre" in normalized_question
        )
    )

    if pregunta_ventas_sucursal:
        nombre_sucursal = obtener_nombre_sucursal(question)

        if not nombre_sucursal:
            return None

        nombre_sucursal_sql = limpiar_texto_sql(nombre_sucursal)

        return f"""
SELECT 
    SUM(DF.ValorTotal) AS TotalVentasUltimoTrimestre
FROM DocumentoFiscal DF
WHERE DF.FechaEmision >= DATEADD(QUARTER, DATEDIFF(QUARTER, 0, GETDATE()) - 1, 0)
  AND DF.FechaEmision < DATEADD(QUARTER, DATEDIFF(QUARTER, 0, GETDATE()), 0)
  AND EXISTS (
      SELECT 1
      FROM DetalleManoDeObra DMO
      INNER JOIN OrdeDeTrabajo OT 
          ON OT.NumeroOrden = DMO.NumeroOrden
      INNER JOIN Diagnostico D 
          ON D.NumeroDiagnostico = OT.NumeroOrden
      INNER JOIN Cita C 
          ON C.NumeroCita = D.NumeroCita
      INNER JOIN Sucursal S 
          ON S.CodigoSucursal = C.CodigoSucursal
      WHERE DMO.CodigoTipoDocumentoFiscal = DF.CodigoTipoDocumentoFiscal
        AND DMO.Serie = DF.Serie
        AND DMO.Numero = DF.Numero
        AND S.NombreSucursal LIKE '%{nombre_sucursal_sql}%'
  )
""".strip()

    # Consulta: total de ventas por tipo de documento fiscal.
    if (
        "total de ventas" in normalized_question
        and "tipo de documento" in normalized_question
    ):
        return """
SELECT
    CodigoTipoDocumentoFiscal,
    SUM(ValorTotal) AS TotalVentas
FROM DocumentoFiscal
GROUP BY CodigoTipoDocumentoFiscal
ORDER BY TotalVentas DESC
""".strip()

    # Consulta: top 10 clientes por ventas.
    # Se usa NIT porque DocumentoFiscal guarda el NIT del cliente.
    if (
        "clientes" in normalized_question
        and "mayor total de ventas" in normalized_question
    ) or (
        "clientes" in normalized_question
        and "mayores ventas" in normalized_question
    ) or (
        "top clientes" in normalized_question
    ):
        return """
SELECT TOP 10
    NIT,
    SUM(ValorTotal) AS TotalVentas
FROM DocumentoFiscal
GROUP BY NIT
ORDER BY TotalVentas DESC
""".strip()

    return None


class NaturalQueryService:
    def process_question(self, payload: NaturalQueryRequest) -> NaturalQueryData:
        """
        Flujo principal usando Ollama.

        Pasos:
        1. Revisar si existe una consulta avanzada conocida.
        2. Si no existe, construir un prompt con el contexto del esquema de DonaldV2.
        3. Pedir a Ollama una consulta SQL SELECT.
        4. Validar que el SQL generado sea solo lectura.
        5. Ejecutar la consulta en SQL Server.
        6. Devolver resultados al frontend.
        """

        predefined_sql = get_predefined_sql(payload.question)

        if predefined_sql:
            print("USANDO SQL PREDEFINIDO")
            generated_sql = predefined_sql
        else:
            prompt = build_sql_prompt(payload.question)
            generated_sql = ollama_client.generate_sql_from_question(prompt)

        print("SQL GENERADO:")
        print(generated_sql)

        safe_sql = validate_select_only(generated_sql)

        print("SQL VALIDADO:")
        print(safe_sql)

        rows = execute_select_query(safe_sql)

        return NaturalQueryData(
            question=payload.question,
            generated_sql=safe_sql,
            rows=rows,
        )


nlq_service = NaturalQueryService()