from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Hash import SHA3_256
from Crypto.Random import get_random_bytes

NONCE_LENGTH = 24
TAG_LENGTH = 16

def encrypt(key:str|bytes, plaintext:str|bytes) -> bytes:
    hashed_key = generate_hashed_key(key)
    plaintext_bytes = to_bytes(plaintext)

    nonce = get_random_bytes(NONCE_LENGTH)
    cipher = ChaCha20_Poly1305.new(key=hashed_key, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext_bytes)

    return nonce + tag + ciphertext

def decrypt(key:str|bytes, ciphertext:bytes) -> bytes:
    hashed_key = generate_hashed_key(key)

    received_nonce = ciphertext[:NONCE_LENGTH]
    received_tag = ciphertext[NONCE_LENGTH:NONCE_LENGTH+TAG_LENGTH]
    received_ciphertext = ciphertext[NONCE_LENGTH+TAG_LENGTH:]

    cipher = ChaCha20_Poly1305.new(key=hashed_key, nonce=received_nonce)
    
    return cipher.decrypt_and_verify(ciphertext=received_ciphertext, received_mac_tag=received_tag)

def generate_hashed_key(key:str|bytes) -> bytes:
    return SHA3_256.new(to_bytes(key)).digest()
    
def to_bytes(obj:str|bytes) -> bytes:
    if type(obj) is str:
        return bytes(obj, "utf-8")
    elif type(obj) is bytes:
        return obj
    else:
        raise TypeError("The provided object could not be converted to a byte array.")