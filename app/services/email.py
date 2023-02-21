from smtplib import SMTP_SSL
from ssl import create_default_context
from typing import Tuple

from app.db.settings import settings


def get_smtp_configuration() -> Tuple[str, int, str, str]:
    """Read and return configurations for smtp server."""
    smtp_server = settings.SMTP_SERVER
    port = settings.SMTP_PORT
    sender_email = settings.SENDER_EMAIL
    mail_password = settings.MAIL_PASSWORD
    return (smtp_server,
            port,
            sender_email,
            mail_password)


async def send_email(receiver_email: str, message: bytes) -> None:
    """Service function for sending email."""
    context = create_default_context()
    smtp_server, port, sender_email, mail_password = (
        get_smtp_configuration()
    )
    with SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, mail_password)
        server.sendmail(sender_email, receiver_email, message)
