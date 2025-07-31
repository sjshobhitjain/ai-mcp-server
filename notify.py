import yagmail
import os

# Set environment variables before running:
# export ALERT_EMAIL_USER="your_email@gmail.com"
# export ALERT_EMAIL_PASSWORD="your_app_password"
# export ALERT_EMAIL_TO="recipient_email@gmail.com"

EMAIL_USER = os.environ.get("ALERT_EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("ALERT_EMAIL_PASSWORD")
EMAIL_TO = os.environ.get("ALERT_EMAIL_TO")

def send_email_alert(agent, event, risk_score, impact, resolution_steps):
    """Send an email with risk and resolution details."""
    if not EMAIL_USER or not EMAIL_PASSWORD or not EMAIL_TO:
        print("⚠️ Email credentials not set. Skipping email notification.")
        return

    yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASSWORD)

    subject = f"[MCP ALERT] {agent} detected risk (Score: {risk_score})"
    body = f"""
    Agent: {agent}
    Event: {event}

    Risk Score: {risk_score}
    Impact: {impact}

    Suggested Steps:
    {resolution_steps}
    """

    try:
        yag.send(EMAIL_TO, subject, body)
        print(f"📧 Email alert sent to {EMAIL_TO}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
