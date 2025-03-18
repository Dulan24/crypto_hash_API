from fastapi import APIRouter, HTTPException
from app.services.key_decryption_services import decrypt_aes, decrypt_rsa
from app.services.db_handler_service import get_private_key_from_db
from app.models import DecryptRequest, DecryptResponse

router = APIRouter()

@router.post("/decrypt", response_model=DecryptResponse)
def decrypt_data(request: DecryptRequest):
    key, stored_algorithm = get_private_key_from_db(request.key_id)

    if not key:
        raise HTTPException(status_code=404, detail="Key not found.")

    if request.algorithm.upper() != stored_algorithm.upper():
        raise HTTPException(status_code=400, detail="Algorithm mismatch. Key was stored for a different algorithm.")

    try:
        if stored_algorithm.upper() == "AES":
            plaintext = decrypt_aes(request.ciphertext, key)
        elif stored_algorithm.upper() == "RSA":
            plaintext = decrypt_rsa(request.ciphertext, key)
        else:
            raise HTTPException(status_code=400, detail="Unsupported decryption algorithm.")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return DecryptResponse(plaintext=plaintext)
