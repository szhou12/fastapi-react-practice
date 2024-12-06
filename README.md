# FastAPI + React

## Index
- [Backend - FastAPI](#backend---fastapi)

## Backend - FastAPI
### 1. Setup conda environment
```linux
$ cd backend
$ conda create --name fastapi-react-prac python=3.10
```
### 2. Install dependencies
```linux
pip install -r requirements.txt
```
Dependency Explanation:
- `uvicorn`: web server that takes `fastapi` code and host that as a web server.
- `python-multipart`: decoding JSON data.
- `python-jose[cryptography]`: signing and verifying JWTs. Implementing OAuth2 or OpenID Connect.
- `passlib[bcrypt]`: password hashing.
- `PyJWT`: encoding and decoding JSON Web Tokens (JWT).
- `python-decouple`: organize configuration settings, especially secrets (e.g. `.env`), outside the source code.