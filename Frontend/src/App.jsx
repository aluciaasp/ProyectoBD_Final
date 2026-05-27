import { useMemo, useState } from "react";
import axios from "axios";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import {
  BarChart3,
  CheckCircle,
  Clipboard,
  Database,
  Loader2,
  MessageSquare,
  Search,
  ShieldCheck,
  Sparkles,
  Table2,
} from "lucide-react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/api/nql/query";

function App() {
  const [question, setQuestion] = useState("Muéstrame 10 clientes");
  const [generatedSql, setGeneratedSql] = useState("");
  const [rows, setRows] = useState([]);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const columns = useMemo(() => {
    if (!rows || rows.length === 0) return [];
    return Object.keys(rows[0]);
  }, [rows]);

  const totalConsultas = history.length;

  const tablasConsultadas = new Set(
    history
      .map((item) => item.sql)
      .join(" ")
      .match(/FROM\s+([a-zA-Z0-9_]+)/gi)
      ?.map((match) => match.replace(/FROM\s+/i, "")) || []
  ).size;

  const numericColumns = useMemo(() => {
    if (!rows || rows.length === 0) return [];

    return columns.filter((column) =>
      rows.some((row) => typeof row[column] === "number")
    );
  }, [rows, columns]);

  const chartData = useMemo(() => {
    if (!rows || rows.length === 0 || numericColumns.length === 0) return [];

    const numericColumn = numericColumns[0];
    const labelColumn = columns.find((column) => column !== numericColumn);

    return rows.map((row, index) => ({
      name: String(row[labelColumn] ?? `Fila ${index + 1}`),
      value: Number(row[numericColumn] ?? 0),
    }));
  }, [rows, columns, numericColumns]);

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!question.trim()) {
      setError("Por favor escribe una pregunta.");
      return;
    }

    setLoading(true);
    setError("");
    setMessage("");

    try {
      const response = await axios.post(API_URL, {
        question: question.trim(),
      });

      const result = response.data;

      setMessage(result.message || "Consulta procesada correctamente");
      setGeneratedSql(result.data?.generated_sql || "");
      setRows(result.data?.rows || []);

      setHistory((prev) => [
        {
          question: question.trim(),
          sql: result.data?.generated_sql || "",
          rows: result.data?.rows?.length || 0,
          date: new Date().toLocaleTimeString(),
        },
        ...prev.slice(0, 4),
      ]);
    } catch (err) {
      const backendMessage =
        err.response?.data?.message ||
        "No se pudo conectar con el backend. Verifica que FastAPI esté encendido.";

      setError(backendMessage);
      setRows([]);
      setGeneratedSql("");
    } finally {
      setLoading(false);
    }
  };

  const useSuggestion = (text) => {
    setQuestion(text);
  };

  const copySql = async () => {
    if (!generatedSql) return;

    try {
      await navigator.clipboard.writeText(generatedSql);
      setMessage("SQL copiado al portapapeles");
      setError("");
    } catch {
      setError("No se pudo copiar el SQL.");
    }
  };

  const formatSql = (sql) => {
    if (!sql) return "";

    return sql
      .replace(/\s+/g, " ")
      .replace(/\bSELECT\b/gi, "SELECT")
      .replace(/\bFROM\b/gi, "\nFROM")
      .replace(/\bWHERE\b/gi, "\nWHERE")
      .replace(/\bAND\b/gi, "\nAND")
      .replace(/\bOR\b/gi, "\nOR")
      .replace(/\bINNER JOIN\b/gi, "\nINNER JOIN")
      .replace(/\bLEFT JOIN\b/gi, "\nLEFT JOIN")
      .replace(/\bRIGHT JOIN\b/gi, "\nRIGHT JOIN")
      .replace(/\bJOIN\b/gi, "\nJOIN")
      .replace(/\bGROUP BY\b/gi, "\nGROUP BY")
      .replace(/\bORDER BY\b/gi, "\nORDER BY")
      .replace(/\bHAVING\b/gi, "\nHAVING")
      .trim();
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <Database size={28} />
          </div>
          <div>
            <h1>Donald-IA</h1>
            <p>Consultas inteligentes para DonaldV2</p>
          </div>
        </div>

        <nav className="menu">
          <button
            className="menu-item active"
            onClick={() =>
              document
                .getElementById("consulta")
                ?.scrollIntoView({ behavior: "smooth" })
            }
          >
            <MessageSquare size={20} />
            Nueva consulta
          </button>

          <button
            className="menu-item"
            onClick={() =>
              document
                .getElementById("graficas")
                ?.scrollIntoView({ behavior: "smooth" })
            }
          >
            <BarChart3 size={20} />
            Gráficas
          </button>
        </nav>

        <div className="db-card">
          <p>Base de datos activa</p>
          <h3>DonaldV2</h3>
          <span>Conectado a SQL Server</span>
        </div>

        <div className="sidebar-footer">Proyecto Final BD II</div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <h2>Sistema inteligente para Talleres Donald</h2>
            <p>Convierte preguntas en lenguaje natural en consultas SQL seguras.</p>
          </div>

          <div className="status-group">
            <div className="status-pill">
              <span className="dot"></span>
              SQL Server
            </div>
            <div className="status-pill">
              <span className="dot"></span>
              Ollama activo
            </div>
          </div>
        </header>

        <section className="content-grid">
          <div className="left-column">
            <section className="card query-card" id="consulta">
              <div className="card-title">
                <Search size={20} />
                <h3>Escribe tu pregunta</h3>
              </div>

              <form onSubmit={handleSubmit}>
                <div className="query-row">
                  <textarea
                    value={question}
                    onChange={(event) => setQuestion(event.target.value)}
                    placeholder="Ejemplo: Muéstrame 10 clientes"
                    maxLength={500}
                  />
                  <button type="submit" disabled={loading}>
                    {loading ? (
                      <>
                        <Loader2 className="spin" size={18} />
                        Consultando
                      </>
                    ) : (
                      <>
                        <Sparkles size={18} />
                        Consultar
                      </>
                    )}
                  </button>
                </div>
              </form>

              <div className="suggestions">
                <span>Sugerencias populares:</span>

                <button
                  onClick={() =>
                    useSuggestion("Muestra el teléfono del cliente con NIT CF-57")
                  }
                >
                  Teléfono por NIT
                </button>

                <button
                  onClick={() =>
                    useSuggestion(
                      "Dime el historial de servicios del vehículo con placa P097TWG"
                    )
                  }
                >
                  Historial por placa
                </button>

                  <button
                  onClick={() =>
                    useSuggestion(
                      "Muéstrame los documentos fiscales emitidos en mayo de 2011"
                    )
                  }
                >
                  Documentos fiscales por fecha
                </button>

                 <button
                  onClick={() =>
                    useSuggestion(
                      "Cuáles son los materiales más utilizados"
                    )
                  }
                >
                  Materiales más utilizados
                </button>

                <button
                  onClick={() =>
                    useSuggestion(
                      "Cuál fue el total de ventas en el último trimestre en la Sucursal Jalapa"
                    )
                  }
                >
                  Ventas último trimestre
                </button>

                <button onClick={() => useSuggestion("Muéstrame 10 clientes")}>
                  Clientes
                </button>
              </div>
            </section>

            {error && <section className="alert error">{error}</section>}

            {message && !error && (
              <section className="alert success">
                <CheckCircle size={18} />
                {message}
              </section>
            )}

            <section className="card sql-card">
              <div className="section-header">
                <div className="card-title">
                  <Clipboard size={20} />
                  <h3>SQL generado</h3>
                </div>

                <button
                  className="small-button"
                  onClick={copySql}
                  disabled={!generatedSql}
                >
                  Copiar SQL
                </button>
              </div>

              <pre>
                {generatedSql
                  ? formatSql(generatedSql)
                  : "Aquí aparecerá la consulta SQL generada por Ollama."}
              </pre>

              <div className="security-note">
                <ShieldCheck size={18} />
                Consulta validada como solo lectura. Se bloquean INSERT, UPDATE,
                DELETE y DROP.
              </div>
            </section>

            <section className="card results-card">
              <div className="section-header">
                <div className="card-title">
                  <Table2 size={20} />
                  <h3>Resultados</h3>
                </div>

                <div className="table-actions">
                  <span>{rows.length} filas</span>
                </div>
              </div>

              {rows.length === 0 ? (
                <div className="empty-state">
                  No hay resultados todavía. Realiza una consulta para ver datos.
                </div>
              ) : (
                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>#</th>
                        {columns.map((column) => (
                          <th key={column}>{column}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {rows.map((row, index) => (
                        <tr key={index}>
                          <td>{index + 1}</td>
                          {columns.map((column) => (
                            <td key={column}>{String(row[column])}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </section>

            <section className="card chart-card" id="graficas">
              <div className="card-title">
                <BarChart3 size={20} />
                <h3>Gráficas</h3>
              </div>

              {rows.length === 0 ? (
                <div className="empty-state">
                  Las gráficas aparecerán cuando ejecutes una consulta con datos
                  numéricos.
                </div>
              ) : numericColumns.length === 0 ? (
                <div className="empty-state">
                  La consulta actual no contiene columnas numéricas suficientes para
                  generar una gráfica.
                </div>
              ) : (
                <div className="chart-container">
                  <p className="chart-description">
                    Gráfica generada con la columna numérica:{" "}
                    <strong>{numericColumns[0]}</strong>
                  </p>

                  <ResponsiveContainer width="100%" height={320}>
                    <BarChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="value" fill="#0b72df" radius={[8, 8, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              )}
            </section>
          </div>

          <aside className="right-column">
            <section className="card summary-card">
              <h3>Resumen de la sesión</h3>

              <div className="metric">
                <div className="metric-icon blue">
                  <Database size={22} />
                </div>
                <div>
                  <p>Consultas ejecutadas</p>
                  <strong>{totalConsultas}</strong>
                </div>
              </div>

              <div className="metric">
                <div className="metric-icon green">
                  <Table2 size={22} />
                </div>
                <div>
                  <p>Tablas consultadas</p>
                  <strong>{tablasConsultadas}</strong>
                </div>
              </div>
            </section>

            <section className="card history-card">
              <h3>Historial reciente</h3>

              {history.length === 0 ? (
                <p className="muted">Aún no hay consultas.</p>
              ) : (
                history.map((item, index) => (
                  <div className="history-item" key={index}>
                    <strong>{item.question}</strong>
                    <span>
                      {item.rows} filas · {item.date}
                    </span>
                  </div>
                ))
              )}
            </section>
          </aside>
        </section>
      </main>
    </div>
  );
}

export default App;