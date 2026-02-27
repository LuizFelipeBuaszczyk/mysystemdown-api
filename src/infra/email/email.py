from enum import Enum
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from utils.logger import get_logger

logger = get_logger(__name__)

class EmailType(Enum):
    CONFIRM_EMAIL_USER = 'confirm-user-email'
    RESET_ACCOUNT_PASSWORD = 'reset-account-password'

class Email:
    
    @classmethod
    def send_email(cls, subject, to_email, email_type: str, context: dict):
        logger.info(f"Sending email to {to_email} - type: {email_type}")
        html_content, html_text = cls.__get_html_template(email_type, context)
        
        email = EmailMultiAlternatives(
            subject=subject, 
            body=html_text, 
            from_email=settings.EMAIL_HOST_USER, 
            to=[to_email]         
            )
        email.attach_alternative(html_content, 'text/html')
        email.send()
        logger.info(f"Email sent to {to_email} - type: {email_type}")
        
    @staticmethod
    def __get_html_template(email_type: str, context: dict):
        logger.debug(f"Starting Email __get_html_template - email_type: {email_type}")
        html_content = render_to_string(f'emails/{email_type}.html', context)
        html_text = strip_tags(html_content)
        return html_content, html_text
        
    