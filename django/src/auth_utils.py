import hashlib
import uuid


def hash_password(password):
    password = bytes(password, 'utf-8')
    encoded_password = hashlib.sha256(password).hexdigest()
    return encoded_password


def generate_token():
    token = uuid.uuid4().hex
    return token

