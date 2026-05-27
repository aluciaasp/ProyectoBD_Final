## Estructura del proyecto

```text
ProyectoBD_Final/
  Backend/
    app/
      main.py
      config.py
      database/
      integrations/
      routes/
      services/
      schemas/
      utils/
    requirements.txt
    .env.example

  Frontend/
    src/
      App.jsx
      App.css
      index.css
      main.jsx
    package.json
    vite.config.js

  README.md
  .gitignore
```

---

## Ejecutar Backend

Abrir una terminal en la carpeta raíz del proyecto y ejecutar:

```bash
cd Backend
python -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

El backend quedará disponible en:

```text
http://127.0.0.1:8000
```

Endpoints disponibles:

```text
GET  /health
POST /api/nql/query
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Ejecutar Frontend

Abrir otra terminal en la carpeta raíz del proyecto y ejecutar:

```bash
cd Frontend
npm install
npm run dev
```

Abrir en el navegador:

```text
http://localhost:5173
```

> Nota: el backend debe estar ejecutándose en `http://127.0.0.1:8000` para que el frontend pueda consultar la API.

Endpoints disponibles:

- `GET /health`
- `POST /api/nlq/query`