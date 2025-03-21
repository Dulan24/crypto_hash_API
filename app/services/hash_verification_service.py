import hashlib
import base64
from app.models import HashVerifyRequest, HashVerifyResponse

# Supported hashing algorithms (same as used for hash generation)
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

def verify_hash(request: HashVerifyRequest) -> HashVerifyResponse:
    # Validate that the provided algorithm is supported
    if request.algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError("Unsupported hashing algorithm")
    
    # Compute the hash for the provided data
    hash_function = SUPPORTED_ALGORITHMS[request.algorithm]()
    hash_function.update(request.data.encode("utf-8"))
    computed_hash_bytes = hash_function.digest()
    computed_hash_base64 = base64.b64encode(computed_hash_bytes).decode("utf-8")
    
    # Compare the computed hash with the provided hash_value
    is_valid = computed_hash_base64 == request.hash_value
    message = "Hash matches the data." if is_valid else "Hash does not match the data."
    
    return HashVerifyResponse(is_valid=is_valid, message=message)
