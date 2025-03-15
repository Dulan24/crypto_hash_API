from pydantic import BaseModel

# DTO for hash generation request
class HashGenRequest(BaseModel):
    data: str
    algorithm: str
    
# DTO for hash gen response responses
class HashGenResponse(BaseModel):
    hash_value: str
    algorithm: str

# DTO for key generation request
class KeyRequest(BaseModel):
    key_type: str
    key_size: int

# DTO for key generation response
class KeyResponse(BaseModel):
    key_id: str
    key_value: str