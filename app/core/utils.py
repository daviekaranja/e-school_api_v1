import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional, Dict

import emails
from emails.template import JinjaTemplate
from jose import jwt
from app.core.config import settings


def send_email(
        email_to: str,
        subject_template: str = '',
        html_template: str = '',
        environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAIL_ENABLED, "no provided configuration"
    message = emails.message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAIL_FROM_NAME, settings.FIRST_SUPERUSER_EMAIL)
    )


def generate_password_reset_token(email: str) -> str:
    """
    generates a token
    :param email:
    :return:
    """
    delta = timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    now = datetime.now()
    print(f"from {__name__} current time is {now}")
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "email": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        print(f'decoded_token:{decoded_token}')
        return decoded_token["email"]
    except jwt.JWTError:
        return None
