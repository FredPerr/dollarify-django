import binascii
from dollarify import db
from dollarify.db import validators
from dollarify.utils import hashing


def insert(email: str, first_name: str, last_name: str, password_raw: str, phone: str = None):

    assert validators.validate_email(email), f'The email address {email} is not valid.'
    assert validators.validate_name(f'{first_name} {last_name}'), f'The name {first_name} {last_name} is not valid.'

    salt, password = hashing.hash_password(password_raw)
    cur = db.CONNECTION.cursor()
    cur.execute("INSERT INTO users (email, first_name, last_name, phone, password, salt) VALUES('%(email)s', '%(first_name)s', '%(last_name)s', '%(phone)s', '%(password)s', '%(salt)s');",
    {
        'email':email, 
        'first_name': first_name, 
        'last_name': last_name, 
        'phone': phone.replace('-', '').replace(' ', ''),
        'password': binascii.hexlify(password).decode(),
        'salt': binascii.hexlify(salt).decode(), 
    })
    cur.close()
    db.CONNECTION.commit()

def get(email: str, columns=['*',]):
    assert validators.validate_email(email)
    cur = db.CONNECTION.cursor()
    columns = ','.join(columns)
    cur.execute(f"SELECT {columns} FROM users WHERE email='{email}';",
    {
        'columns': ','.join(columns),
        'email': email
    })
    user = cur.fetchone()
    cur.close()
    return user



