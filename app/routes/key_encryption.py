from fastapi import FastAPI, HTTPException
from app.services.key_encryption_service import encrypt_aes, encrypt_rsa
from app.services.db_handler_service import get_key_from_db
from app.models import EncryptRequest, EncryptResponse
from fastapi import APIRouter

router = APIRouter()

@router.post("/encrypt", response_model=EncryptResponse)
def encrypt_data(request: EncryptRequest):
    """Encrypts data using AES or RSA based on stored key."""
    key, stored_algorithm = get_key_from_db(request.key_id)

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