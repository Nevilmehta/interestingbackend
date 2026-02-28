import smtplib, time
from email.message import EmailMessage
from core.config import settings
from core.celery_app import celery_app

# retry_backoff scales automatically
@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3, "countdown": 5})
def send_welcome_email(self, email: str):
    print("🔥 TASK STARTED FOR:", email)

    msg = EmailMessage()
    msg["Subject"] = "Welcome to Backend Concepts 🚀"
    msg["From"] = settings.FROM_EMAIL
    msg["To"] = email

    msg.set_content(
        f"""
Hi 👋,

Welcome to Backend Concepts!
Your account has been created successfully.

Happy coding 🚀
"""
    )

    
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        # server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.login("wrong", "wrong")
        server.send_message(msg)

    print(f"[CELERY EMAIL] Sent welcome email to {email}")



