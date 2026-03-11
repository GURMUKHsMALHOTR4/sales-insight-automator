# Sales Insight Automator

Upload sales data (CSV/XLSX), get an AI-generated executive summary, and receive it by email.

---

## Quick start

### Option 1: Docker (recommended)

```bash
# Create backend/.env with your RESEND_API_KEY (see backend/.env.example)
cp backend/.env.example backend/.env
# Edit backend/.env and set RESEND_API_KEY=your_key

docker compose up --build
```

- **Frontend:** http://localhost:3000  
- **Backend / Swagger:** http://localhost:8000/docs  

### Option 2: Local run

**Backend**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # Edit .env and set RESEND_API_KEY
uvicorn app.main:app --reload --port 8000
```

**Frontend** (in another terminal)

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000. Set `NEXT_PUBLIC_API_URL=http://localhost:8000` in `frontend/.env.local` if the API is on another host.

---

## Secured endpoints

- **Rate limiting:** `POST /api/insight` is limited to **10 requests per minute per IP** (configurable via SlowAPI).
- **Input validation:** File type restricted to `.csv` and `.xlsx`; max size 10 MB, max 10k rows; **email format** validated before processing.
- **CORS:** Allowed origins are set via `CORS_ORIGINS` (comma-separated). Default: `http://localhost:3000`.
- **Secrets:** API keys (Resend, etc.) are read from environment only; never logged or returned in responses.

---

## API

- **GET /health** — Health check for load balancers.
- **POST /api/insight** — Upload a file and recipient email (form-data: `file`, `recipient_email`). Returns summary and sends email when `RESEND_API_KEY` is set.

Live docs: **http://localhost:8000/docs** (Swagger) and **http://localhost:8000/redoc**.

---

## Environment (backend)

| Variable           | Required | Description                                      |
|--------------------|----------|--------------------------------------------------|
| `RESEND_API_KEY`   | Yes*     | Resend API key to send email. *Optional: app works without it but won’t send. |
| `CORS_ORIGINS`     | No       | Comma-separated origins. Default: `http://localhost:3000` |
| `OLLAMA_BASE_URL`  | No       | Ollama URL for AI summary. Default: `http://localhost:11434` |
| `OLLAMA_MODEL`     | No       | Model name. Default: `llama3.2`                 |

See **backend/.env.example** for a template.

---

## Project layout

```
├── backend/          # FastAPI app (parser, LLM, email, security)
├── frontend/         # Next.js SPA (upload form, email, states)
├── sample_data/      # Example CSV for testing
├── docker-compose.yml
└── .github/workflows/ci.yml   # CI on PR to main (lint + build)
```

---

## CI/CD

On **pull requests to `main`**, GitHub Actions:

- **Backend:** install deps, run Ruff lint, import-check the app.
- **Frontend:** install deps, run ESLint, run `npm run build`.

No secrets required for CI.

---

<img width="1555" height="808" alt="Screenshot 2026-03-11 at 9 51 43 AM" src="https://github.com/user-attachments/assets/c468931c-0572-4c8e-b2a6-556d8a043e8e" />
<img width="1393" height="800" alt="Screenshot 2026-03-11 at 9 51 07 AM" src="https://github.com/user-attachments/assets/f4ea09f1-3cfe-424d-8a0a-4f2e0205aa30" />

