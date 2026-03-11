"""
Sales Insight Automator - FastAPI backend.
Provides health check and insight generation endpoint.
"""
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.services.parser import parse_sales_file
from app.services.llm import generate_sales_summary
from app.services.email import send_sales_summary_email

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
    Parses the file, generates a summary, and sends it to the recipient (if RESEND_API_KEY is set).
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

    try:
        summary = generate_sales_summary(records)
    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": f"Summary generation failed: {e}"}

    email_sent, email_message = send_sales_summary_email(recipient_email, summary, file.filename or "sales_data")

    return {
        "success": True,
        "message": "Summary generated" + (" and sent by email." if email_sent else "."),
        "filename": file.filename,
        "recipient_email": recipient_email,
        "rows_parsed": len(records),
        "summary": summary,
        "email_sent": email_sent,
        "email_message": email_message,
    }
