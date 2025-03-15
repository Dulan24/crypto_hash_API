from fastapi import FastAPI
from app.routes import hash_generation_route

app = FastAPI(
    title="Cybersecurity API",
    description="API for cybersecurity operations",
    version="0.1"
)

app.include_router(hash_generation_route.router)

# Root Endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Hash API!"}