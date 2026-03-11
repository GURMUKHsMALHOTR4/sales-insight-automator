"""
Parse CSV and XLSX sales data into structured records for the LLM.
"""
import io
from typing import Any

import pandas as pd


ALLOWED_EXTENSIONS = {"csv", "xlsx"}
MAX_ROWS = 10_000
MAX_FILE_BYTES = 10 * 1024 * 1024  # 10 MB


def parse_sales_file(content: bytes, filename: str) -> list[dict[str, Any]]:
    """
    Parse uploaded file (CSV or XLSX) into a list of row dicts.
    Raises ValueError on invalid/empty data or size limits.
    """
    if len(content) > MAX_FILE_BYTES:
        raise ValueError(f"File too large. Maximum size is {MAX_FILE_BYTES // (1024*1024)} MB.")

    ext = (filename or "").lower().split(".")[-1]
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Only .csv and .xlsx are allowed. Got: {ext}")

    try:
        if ext == "csv":
            df = pd.read_csv(io.BytesIO(content), nrows=MAX_ROWS)
        else:
            df = pd.read_excel(io.BytesIO(content), engine="openpyxl", nrows=MAX_ROWS)
    except Exception as e:
        raise ValueError(f"Could not parse file: {e}") from e

    if df.empty or len(df) == 0:
        raise ValueError("File has no data rows.")

    # Normalize: strip column names, fill NaN for consistent JSON
    df.columns = df.columns.astype(str).str.strip()
    records = df.fillna("").astype(str).to_dict(orient="records")

    return records
