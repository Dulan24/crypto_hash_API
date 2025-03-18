from fastapi import FastAPI, HTTPException
from app.services.key_encryption_service import encrypt_aes, encrypt_rsa
from app.services.db_handler_service import get_public_key_from_db, get_private_key_from_db
from app.models import EncryptRequest, EncryptResponse
from fastapi import APIRouter
import base64

router = APIRouter()

@router.post("/encrypt", response_model=EncryptResponse)
def encrypt_data(request: EncryptRequest):
    """Encrypts data using AES or RSA based on stored key."""

    key, stored_algorithm = None, None  

    if request.algorithm.upper() == "AES":
        key, stored_algorithm = get_private_key_from_db(request.key_id)
    elif request.algorithm.upper() == "RSA":
        key, stored_algorithm = get_public_key_from_db(request.key_id)
    else:
        raise HTTPException(status_code=400, detail="Unsupported encryption algorithm. Choose AES or RSA.")

    if not key:
        raise HTTPException(status_code=404, detail="Key not found.")

    if request.algorithm.upper() != stored_algorithm.upper():
        raise HTTPException(status_code=400, detail="Algorithm mismatch. Key was stored for a different algorithm.")

    if stored_algorithm.upper() == "AES":
        ciphertext = encrypt_aes(request.plaintext, key)
    elif stored_algorithm.upper() == "RSA":
        ciphertext = encrypt_rsa(request.plaintext, key)
    else:
        raise HTTPException(status_code=400, detail="Unsupported encryption algorithm.")

    return EncryptResponse(ciphertext=ciphertext)
