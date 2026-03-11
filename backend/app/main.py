"""
Sales Insight Automator - FastAPI backend.
Provides health check and insight generation endpoint.
"""
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.services.parser import parse_sales_file

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
    Parses the file; LLM summary and email will be wired in next steps.
    """
    if not file.filename:
        return {"success": False, "error": "No file provided"}

    try:
        content = await file.read()
    except Exception as e:
        return {"success": False, "error": f"Failed to read file: {e}"}

    try:
        records = parse_sales_file(content, file.filename)
    except ValueError as e:
        return {"success": False, "error": str(e)}

    return {
        "success": True,
        "message": "File parsed successfully",
        "filename": file.filename,
        "recipient_email": recipient_email,
        "rows_parsed": len(records),
        "columns": list(records[0].keys()) if records else [],
    }
