"""
Send the sales summary to the recipient via Resend.
When RESEND_API_KEY is not set, no email is sent (app still returns success).
"""
import os


def send_sales_summary_email(to_email: str, summary: str, filename: str) -> tuple[bool, str]:
    """
    Send the generated summary to the given email address.
    Returns (sent: bool, message: str).
    """
    api_key = (os.getenv("RESEND_API_KEY") or "").strip()
    if not api_key:
        return False, "RESEND_API_KEY not set; email skipped. Set it to enable delivery."

    from_address = os.getenv("RESEND_FROM", "Sales Insight <onboarding@resend.dev>")
    subject = f"Sales Insight: {filename}"

    try:
        import resend
        resend.api_key = api_key
        resend.Emails.send({
            "from": from_address,
            "to": [to_email],
            "subject": subject,
            "text": summary,
        })
        return True, "Email sent successfully."
    except Exception as e:
        return False, str(e)
