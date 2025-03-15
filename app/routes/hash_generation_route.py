from fastapi import APIRouter, HTTPException
from app.models import HashGenRequest, HashGenResponse
from app.services.hash_generation_service import generate_hash

router = APIRouter()

@router.post("/generate-hash", response_model=HashGenResponse)
def generate_hash_api(request: HashGenRequest):
    try:
        return generate_hash(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
