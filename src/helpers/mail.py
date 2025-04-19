import os
from typing import Dict

from pydantic import EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi.templating import Jinja2Templates

from src.settings import EmailEnv

conf = ConnectionConfig(
    MAIL_USERNAME=EmailEnv.MAIL_USERNAME,
    MAIL_PASSWORD=EmailEnv.MAIL_PASSWORD,
    MAIL_FROM=EmailEnv.MAIL_FROM,
    MAIL_PORT=EmailEnv.MAIL_PORT,
    MAIL_SERVER=EmailEnv.MAIL_SERVER,
    MAIL_STARTTLS=EmailEnv.MAIL_STARTTLS,
    MAIL_SSL_TLS=EmailEnv.MAIL_SSL_TLS,
    USE_CREDENTIALS=EmailEnv.USE_CREDENTIAL,
)


templates_path = os.path.join(os.getcwd(), 'src', 'views')
templates = Jinja2Templates(directory=templates_path)

async def send_mail(subject: str, email_to: EmailStr, body: Dict | None = None):
    html_content = templates.get_template('mail_message.html').render(body)

    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=html_content,
        subtype=MessageType.html,
    )

    fastapi_mail_message_client = FastMail(conf)
    await fastapi_mail_message_client.send_message(message)