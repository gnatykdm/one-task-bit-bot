# service/smtp.py
import aiosmtplib
from datetime import datetime
from email.mime.text import MIMEText
from bot.utills import validate_text
from config import SmtpData, get_smtp_data
from messages import USER_FEEDBACK_MAIL_TEXT

smtp_data: SmtpData = get_smtp_data()
if not smtp_data:
    raise Exception("[ERROR] - SMTP data not found.")

class SmtpService:
    @staticmethod
    async def send_feedback_message(user_message: str, user_id: int, user_name: str):
        if not validate_text(user_message):
            print("[ERROR] - Invalid message.")
            return

        email_body: str = USER_FEEDBACK_MAIL_TEXT.format(
            feedback=user_message,
            username=user_name,
            user_id=user_id,
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        email_message = MIMEText(email_body, "plain")
        email_message['Subject'] = smtp_data.smtp_subject
        email_message['From'] = smtp_data.smtp_from
        email_message['To'] = smtp_data.smtp_receiver

        try:
            await aiosmtplib.send(
                email_message,
                hostname=smtp_data.smtp_host,
                port=smtp_data.smtp_port,
                start_tls=True,
                username=smtp_data.smtp_user,
                password=smtp_data.smtp_password,
            )
            print("[INFO] - Feedback message sent successfully.")
        except Exception as e:
            print(f"[ERROR] - Failed to send feedback message: {e}")
