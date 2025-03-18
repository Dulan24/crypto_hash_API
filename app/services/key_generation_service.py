from fastapi import HTTPException
import base64
import os
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from app.services.db_handler_service import store_aes_key_in_db, store_rsa_keys_in_db


def generate_aes_key(key_size: int, key_id: str):
    if key_size not in [128, 192, 256]:
        raise HTTPException(status_code=400, detail="Invalid AES key size. Choose 128, 192, or 256 bits.")
    key = os.urandom(key_size // 8)
    store_aes_key_in_db(key_id, base64.b64encode(key).decode())
    return base64.b64encode(key).decode()

def generate_rsa_key(key_size: int , key_id: str):
    if key_size not in [2048, 3072, 4096]:
        raise HTTPException(status_code=400, detail="Invalid RSA key size. Choose 2048, 3072, or 4096 bits.")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    store_rsa_keys_in_db(key_id, base64.b64encode(private_pem).decode(), base64.b64encode(public_pem).decode())
    return base64.b64encode(public_pem).decode()

def generate_ec_key(curve: str):
    if curve not in ["secp256r1", "secp384r1", "secp521r1"]:
        raise HTTPException(status_code=400, detail="Invalid elliptic curve. Choose secp256r1, secp384r1, or secp521r1.")
    private_key = ec.generate_private_key(
        ec.SECP256R1(),
        default_backend()
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return base64.b64encode(private_pem).decode()

