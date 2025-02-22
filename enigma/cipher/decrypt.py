from base64 import b64decode
from enigma.cipher.primitive import decrypt

def decrypt_from_bytes_to_bytes(key:str|bytes, ciphertext:bytes):
    return decrypt(key=key, ciphertext=ciphertext)

def decrypt_from_bytes_to_utf8(key:str|bytes, ciphertext:bytes):
    return str(decrypt(key=key, ciphertext=ciphertext), "utf-8")

def decrypt_from_base64_to_bytes(key:str|bytes, ciphertext:str):
    return decrypt(key=key, ciphertext=b64decode(ciphertext))

def decrypt_from_base64_to_utf8(key:str|bytes, ciphertext:str):
    return str(decrypt(key=key, ciphertext=b64decode(ciphertext)), "utf-8")