"""
Generate executive sales summary from structured data.
Uses Ollama (local, no API key) when available; otherwise returns a mock summary.
Install: https://ollama.com — then run: ollama run llama3.2
"""
import json
import os
from collections import Counter
from typing import Any

import httpx

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_TIMEOUT = 120.0


def _generate_mock_summary(records: list[dict[str, Any]]) -> str:
    """Build a simple summary from the data when no LLM is available."""
    if not records:
        return "No sales data to summarize."

    total_revenue = 0
    regions: Counter[str] = Counter()
    products: Counter[str] = Counter()
    statuses: Counter[str] = Counter()

    for row in records:
        r = row.get("Revenue") or row.get("revenue") or 0
        try:
            total_revenue += int(float(r))
        except (TypeError, ValueError):
            pass
        region = str(row.get("Region") or row.get("region") or "").strip()
        if region:
            regions[region] += 1
        product = str(row.get("Product_Category") or row.get("product_category") or "").strip()
        if product:
            products[product] += 1
        status = str(row.get("Status") or row.get("status") or "").strip()
        if status:
            statuses[status] += 1

    top_region = regions.most_common(1)[0][0] if regions else "N/A"
    top_product = products.most_common(1)[0][0] if products else "N/A"

    lines = [
        f"• Total records analyzed: {len(records)}.",
        f"• Total revenue (from data): ${total_revenue:,}.",
        f"• Top region by transaction count: {top_region}.",
        f"• Top product category: {top_product}.",
        f"• Order status breakdown: {dict(statuses) if statuses else 'N/A'}.",
        "• Tip: Run 'ollama run llama3.2' locally for AI-generated summaries.",
    ]
    return "\n".join(lines)


def _build_prompt(records: list[dict[str, Any]]) -> str:
    data_sample = records[:500]
    data_str = json.dumps(data_sample, indent=0)
    return f"""You are a sales analyst. Given the following sales data (JSON rows), write a concise executive summary.

Requirements:
- 3 to 5 bullet points
- Professional tone suitable for leadership
- Highlight: total revenue, top region/product, notable trends, and one brief recommendation
- No markdown, plain text only

Sales data:
{data_str}

Executive summary:"""


def generate_sales_summary(records: list[dict[str, Any]]) -> str:
    """
    Produce a short executive summary from sales records.
    Uses local Ollama if available (no API key); otherwise returns a mock summary.
    """
    base = (os.getenv("OLLAMA_BASE_URL") or OLLAMA_BASE_URL).rstrip("/")
    model = os.getenv("OLLAMA_MODEL") or OLLAMA_MODEL
    url = f"{base}/api/generate"
    payload = {
        "model": model,
        "prompt": _build_prompt(records),
        "stream": False,
    }

    try:
        with httpx.Client(timeout=OLLAMA_TIMEOUT) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            content = (data.get("response") or "").strip()
            if content:
                return content
    except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPStatusError, Exception):
        pass

    return _generate_mock_summary(records)
