from fastapi import FastAPI
from app.routes import hash_generation_route, hash_verification_route, key_generation, key_encryption, key_decryption
from app.services.db_handler_service import create_database, create_table, get_db_connection

print("Setting up the database...")
# create_database()
create_table()
get_db_connection()
print("Database setup complete.")

app = FastAPI(
    title="Cybersecurity API",
    description="API for cybersecurity operations",
    version="0.1"
)

app.include_router(hash_generation_route.router)
app.include_router(key_generation.router)
app.include_router(key_encryption.router)
app.include_router(key_decryption.router)
app.include_router(hash_verification_route.router)

# Root Endpoint
@app.get("/")
def root():
    return {"message": "Cryptographic API is running"}
