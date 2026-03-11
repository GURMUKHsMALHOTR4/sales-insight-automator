"""
Sales Insight Automator - FastAPI backend.
Provides health check and insight generation endpoint (stub).
"""
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sales Insight Automator API",
    description="Upload sales data, get AI-generated summary, receive it by email.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """Health check for load balancers and monitoring."""
    return {"status": "ok"}


@app.post("/api/insight")
async def create_insight(
    file: UploadFile = File(...),
    recipient_email: str = Form(...),
):
    """
    Upload a sales data file (CSV or XLSX) and recipient email.
    Returns a placeholder until parser + LLM + email are wired.
    """
    # Stub: validate file type
    if not file.filename:
        return {"success": False, "error": "No file provided"}
    ext = (file.filename or "").lower().split(".")[-1]
    if ext not in ("csv", "xlsx"):
        return {"success": False, "error": "Only .csv and .xlsx files are allowed"}

    return {
        "success": True,
        "message": "Stub: file received",
        "filename": file.filename,
        "recipient_email": recipient_email,
    }
