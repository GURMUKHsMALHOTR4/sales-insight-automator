"""
Security: rate limiting and validation helpers.
"""
import os
import re

# CORS origins from env (comma-separated), default localhost:3000
def get_cors_origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", "http://localhost:3000")
    return [x.strip() for x in raw.split(",") if x.strip()]


# Simple email validation (RFC-style); for strict use use pydantic EmailStr
EMAIL_RE = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def is_valid_email(value: str) -> bool:
    if not value or len(value) > 254:
        return False
    return bool(EMAIL_RE.match(value.strip()))
