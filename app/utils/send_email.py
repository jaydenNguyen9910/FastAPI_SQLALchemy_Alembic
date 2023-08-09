from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pydantic import BaseModel
import smtplib

from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.core.settings import settings

SYSTEM_EMAIL = settings.SYSTEM_EMAIL
SYSTEM_EMAIL_PASSWORD = settings.SYSTEM_EMAIL_PASSWORD

# Templates
USER_VERIFICATION_TEMPLATE = """
<html>
    <body>
        <h1>{title}</h1>
        <p>Your verification code is:</p>
        <strong>{verification_code}</strong> 
        <p>Please do not share it with anyone.</p>
    </body>
</html>"""


class EmailBody(BaseModel):
    to: str
    subject: str
    message: str


async def send_email(*, to: str, subject: str, template: str, **kwargs):
    # try:
    msg = MIMEMultipart()
    msg['From'] = SYSTEM_EMAIL
    msg['To'] = to
    msg['Subject'] = subject
    formatted_template = template.format(**kwargs)
    msg.attach(MIMEText(formatted_template, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SYSTEM_EMAIL, SYSTEM_EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()
    return {"message": "Email sent successfully"}

# except Exception as e:
#     raise error_exception_handler(
#         error=Exception(), app_status=AppStatus.EMAIL_SENDING_ERROR)
