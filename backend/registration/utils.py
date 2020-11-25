import scrypt
from base64 import b64encode
from typing import Tuple, List
from email_validator import validate_email, EmailNotValidError

from settings import SALT


def get_request_data(request_data, params: Tuple[str, ...]) -> List[str]:

    if isinstance(request_data, dict):
        result = [request_data.get(param) for param in params]
    else:
        result = [None for _ in params]

    return result


def email_valid(email: str) -> bool:
    try:
        validate_email(email)
        valid = True
    except EmailNotValidError:
        valid = False
    return valid


def password_valid(password: str, min_length: int = 6) -> bool:
    return password.isascii() and len(password) >= min_length


def encrypt_password(password: str) -> bytes:
    _password = password + SALT
    encrypted_password = scrypt.hash(_password, SALT)
    return b64encode(encrypted_password)
