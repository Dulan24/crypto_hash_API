from fastapi import APIRouter, HTTPException
import uuid
import os
from app.models import KeyRequest, KeyResponse
from app.services.key_generation_service import generate_aes_key, generate_rsa_key

router = APIRouter()

@router.post("/generate_key", response_model=KeyResponse)
def generate_key(request: KeyRequest):
    key_id = str(uuid.uuid4())  # Generate a unique key ID
    
    if request.key_type.upper() == "AES":
        key_value = generate_aes_key(request.key_size)
    elif request.key_type.upper() == "RSA":
        key_value = generate_rsa_key(request.key_size)
    else:
        raise HTTPException(status_code=400, detail="Unsupported key type. Supported types: AES, RSA.")
    
    return KeyResponse(key_id=key_id, key_value=key_value)