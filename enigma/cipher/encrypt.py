from base64 import b64encode
from enigma.cipher.primitive import encrypt

def encrypt_to_bytes(key:str|bytes, plaintext:str|bytes):
    return encrypt(key=key, plaintext=plaintext)

def encrypt_to_base64(key:str|bytes, plaintext:str|bytes):
    return b64encode(encrypt(key=key, plaintext=plaintext)).decode("utf-8")