import base64
import os
import psycopg2
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

def encrypt_aes(plaintext: str, key: bytes) -> str:
    """Encrypts plaintext using AES-CBC."""
    iv = os.urandom(16)  
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Ensure plaintext is a multiple of 16 bytes (PKCS7 padding)
    pad_length = 16 - (len(plaintext) % 16)
    padded_plaintext = plaintext + chr(pad_length) * pad_length

    ciphertext = encryptor.update(padded_plaintext.encode()) + encryptor.finalize()

    return base64.b64encode(iv + ciphertext).decode()  # Encode IV + ciphertext

# def encrypt_ctr(plaintext: str, key: bytes) -> str:
#     nonce = os.urandom(16)  # Secure random nonce
#     cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
#     encryptor = cipher.encryptor()

#     ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
#     return base64.b64encode(nonce + ciphertext).decode()

def encrypt_rsa(plaintext: str, public_key_bytes: bytes) -> str:
    """Encrypts plaintext using RSA-OAEP."""
    public_key = serialization.load_pem_public_key(public_key_bytes, backend=default_backend())

    ciphertext = public_key.encrypt(
        plaintext.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return base64.b64encode(ciphertext).decode()