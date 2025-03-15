import hashlib
import base64
from app.models import HashGenRequest, HashGenResponse

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

def generate_hash(request: HashGenRequest) -> HashGenResponse:
    if request.algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError("Unsupported hashing algorithm")
    
    hash_function = SUPPORTED_ALGORITHMS[request.algorithm]()
    hash_function.update(request.data.encode("utf-8"))
    hash_bytes = hash_function.digest()
    
    hash_base64 = base64.b64encode(hash_bytes).decode("utf-8")
    return HashGenResponse(hash_value=hash_base64, algorithm=request.algorithm)
