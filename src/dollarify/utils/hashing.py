import hashlib
import os

def generate_salt(length=32):
    return os.urandom(length)


def hash_password(raw_password, salt=generate_salt(), iterations=100000):
    
    return salt, hashlib.pbkdf2_hmac(
        'sha256',
        raw_password.encode('utf-8'),
        salt,
        iterations,
        dklen=128
    )

def check_password(raw_input, salt, hashed_password, iterations=100000) -> bool:
    new_hashed = hash_password(raw_input, salt, iterations)[-1]
    return new_hashed == hashed_password

