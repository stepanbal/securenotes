import base64
import os
from typing import Tuple

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def encoding(text: str, password: str) -> Tuple[bytes, bytes]:
    password: bytes = bytes(password, encoding='utf8')
    salt: bytes = os.urandom(16)

    kdf: PBKDF2HMAC = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    key: bytes = base64.urlsafe_b64encode(kdf.derive(password))
    f: Fernet = Fernet(key)
    token: bytes = f.encrypt(text.encode('utf-8'))

    return salt, token


def decoding(salt: bytes, password: str, token: bytes):
    kdf: PBKDF2HMAC = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    password: bytes = bytes(password, encoding='utf8')
    key: bytes = base64.urlsafe_b64encode(kdf.derive(password))
    f: Fernet = Fernet(key)
    try:
        text: str = f.decrypt(token).decode('utf-8')
    except InvalidToken:
        text = 'Error. Wrong password'
    return text
