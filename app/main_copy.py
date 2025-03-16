from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib
import base64

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

# Request Structure
class HashRequest(BaseModel):
    data: str
    algorithm: str

# Supported hashing algorithms
# Supported hashing algorithms
SUPPORTED_ALGORITHMS = {
    "SHA-256": hashlib.sha256,
    "SHA-512": hashlib.sha512,
    "SHA-1": hashlib.sha1,
    "MD5": hashlib.md5,
    "SHA-224": hashlib.sha224,
    "SHA-384": hashlib.sha384,
    "BLAKE2b": hashlib.blake2b,
    "BLAKE2s": hashlib.blake2s
}

@app.post("/generate-hash")
def generate_hash(request: HashRequest):
    if request.algorithm not in SUPPORTED_ALGORITHMS:
        raise HTTPException(status_code=400, detail="Unsupported hashing algorithm")
    
    # Compute hash
    hash_function = SUPPORTED_ALGORITHMS[request.algorithm]()
    hash_function.update(request.data.encode("utf-8"))
    hash_bytes = hash_function.digest()
    
    # Convert hash to Base64
    hash_base64 = base64.b64encode(hash_bytes).decode("utf-8")
    
    return {"hash_value": hash_base64, "algorithm": request.algorithm}
