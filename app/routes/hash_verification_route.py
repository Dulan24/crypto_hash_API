from fastapi import APIRouter, HTTPException
from app.models import HashVerifyRequest, HashVerifyResponse
from app.services.hash_verification_service import verify_hash

router = APIRouter()

@router.post("/verify-hash", response_model=HashVerifyResponse)
def verify_hash_api(request: HashVerifyRequest):
    try:
        return verify_hash(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
