import base64
import os

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def encoding(text, password):
    password = bytes(password, encoding='utf8')
    salt = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    token = f.encrypt(text.encode('utf-8'))

    return salt, token


def decoding(salt, password, token):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    password = bytes(password, encoding='utf8')
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    try:
        text = f.decrypt(token).decode('utf-8')
    except InvalidToken:
        text = 'Error. Wrong password'
    return text
