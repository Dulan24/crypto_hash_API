from fastapi import FastAPI
from app.routes import hash_generation_route
from app.routes import key_generation

app = FastAPI(
    title="Cybersecurity API",
    description="API for cybersecurity operations",
    version="0.1"
)

app.include_router(hash_generation_route.router)
app.include_router(key_generation.router)
# Root Endpoint
@app.get("/")
def root():
    return {"message": "Cryptographic API is running"}