from django.conf import settings
from django.core.mail import send_mail
import os
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email_confirmation_token(email, token):
    subject = "Confirm your email"
    token = f"{email},{token}"
    base_url = os.getenv("BASE_URL")
    html_message = render_to_string(
        "authentication/Email.html", {"base_url": base_url, "token": token}
    )
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [email],
        False,
        settings.EMAIL_HOST_USER,
        settings.EMAIL_HOST_PASSWORD,
    )
