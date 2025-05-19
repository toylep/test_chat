from email.message import EmailMessage
import aiosmtplib
from chat.src.core.config import settings

async def send_email(to: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = settings.email.SMTP_USER
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=settings.email.SMTP_HOST,
        port=settings.email.SMTP_PORT,
        start_tls=True,
        username=settings.email.SMTP_USER,
        password=settings.email.SMTP_PASSWORD,
    )
