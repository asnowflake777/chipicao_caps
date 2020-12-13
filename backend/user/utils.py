import scrypt
from base64 import b64encode

from settings import SALT


def password_valid(password: str, min_length: int = 6) -> bool:
    return password.isascii() and len(password) >= min_length


def encrypt_password(password: str) -> bytes:
    _password = password + SALT
    encrypted_password = scrypt.hash(_password, SALT)
    return b64encode(encrypted_password)
