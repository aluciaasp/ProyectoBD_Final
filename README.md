```text
donald-nql/
  backend/
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
    .env
    README.md
```            


## Ejecutar backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Endpoints disponibles:

- `GET /health`
- `POST /api/nlq/query`