import os
from flask import current_app
from enigma.cipher.encrypt import encrypt_to_bytes
from enigma.cipher.decrypt import decrypt_from_bytes_to_bytes
from Crypto.Hash import SHA256
from werkzeug.datastructures.file_storage import FileStorage

MAGIC_NUMBER = bytearray("EROSION", "utf-8") + bytearray([0xcc])

def encrypt_file(key:str|bytes, data:bytes, filename:str, path:str):
    formated_filename = bytearray(filename, "utf-8")[:255]
    plaintext = bytes([len(formated_filename)]) + bytearray(formated_filename) + bytearray(data)
    ciphertext = bytes(MAGIC_NUMBER + bytearray(encrypt_to_bytes(key=key, plaintext=plaintext)))

    checksum = SHA256.new(ciphertext).hexdigest()
    processed_filename = f"{checksum}.ero"

    with open(os.path.join(path, processed_filename), "wb") as cipher_file:
        cipher_file.write(ciphertext)

    return processed_filename

def decrypt_file(key:str|bytes, path:str):
    with open(path, "rb") as erosion:
        ciphertext = erosion.read()

    received_plaintext = decrypt_from_bytes_to_bytes(key=key, ciphertext=ciphertext[len(MAGIC_NUMBER):])

    plaintext = received_plaintext[received_plaintext[0]+1:]
    filename = str(received_plaintext[1:received_plaintext[0]+1], "utf-8")

    return plaintext, filename
    