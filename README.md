# API running on localhost
Cryptographic API and Hash API development.
Use the dd branch for localhost running.
Use the master branch for deployed API.

## Features  

### Hash Generation API
- Supports multiple hashing algorithms (SHA-256, SHA-512, MD5, etc.).  
- Returns Base64-encoded hashes.  
- Verifies hashes against original data.  

---

## Installation  
### 1. Clone the Repository(dd branch)  
```sh
git clone --branch dd https://github.com/Dulan24/crypto_hash_API.git
cd crypto_hash_API
```
### 2. Install required 
```sh
pip install -r requirements.txt
```

### 3. Install PostgreSQL
After installing edit the ```config.py``` code to set the your variables.

### 4. Running command
```
uvicorn app.main:app --reload
```


# Deployed API
The 5 endpoints and database are deployed on render platform. This is currently deployed on a free account which has a higher latency and automatic shutdown once no requests for a certain time. 
Please contact for redeploying the server if deactivated.
```
Dulanlokugeegana@gmail.com
```

### Hosted link
Below link can be use to access the endpoints.

```
https://crypto-hash-api.onrender.com
```

To test with swagger use 
```
https://crypto-hash-api.onrender.com/docs
```