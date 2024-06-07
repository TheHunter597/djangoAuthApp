from django.conf import settings
from django.core.mail import send_mail
import os


def send_password_reset_token(email, token):
    subject = "Reset you password"
    token = f"{email},{token}"
    base_url = os.getenv("BASE_URL")
    message = f"Click this link to reset your password: {base_url}/auth/reset-password/{token}/"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
