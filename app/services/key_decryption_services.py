import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

def decrypt_aes(ciphertext: str, key: bytes) -> str:
    try:
        decoded_data = base64.b64decode(ciphertext)
        iv = decoded_data[:16]  # Extract Initiialization Vector from the first 16 bytes
        encrypted_message = decoded_data[16:]

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(encrypted_message) + decryptor.finalize()

        # Remove PKCS7 padding
        pad_length = padded_plaintext[-1]
        plaintext = padded_plaintext[:-pad_length].decode()

        return plaintext
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")

def decrypt_rsa(ciphertext: str, private_key_bytes: bytes) -> str:
    try:
        private_key = serialization.load_pem_private_key(
            private_key_bytes,
            password=None,
            backend=default_backend()
        )

        decrypted_message = private_key.decrypt(
            base64.b64decode(ciphertext),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return decrypted_message.decode()
    except Exception as e:
        raise ValueError(f"RSA Decryption failed: {str(e)}")
