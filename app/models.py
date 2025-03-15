from pydantic import BaseModel

# DTO for hash generation request
class HashGenRequest(BaseModel):
    data: str
    algorithm: str
    
# DTO for hash gen response responses
class HashGenResponse(BaseModel):
    hash_value: str
    algorithm: str

# DTO for hash verification request
class HashVerifyRequest(BaseModel):
    data: str
    hash_value: str
    algorithm: str

# DTO for hash verification response
class HashVerifyResponse(BaseModel):
    is_valid: bool
    message: str