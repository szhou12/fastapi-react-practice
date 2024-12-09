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
- `PyJWT`: encoding and decoding JSON Web Tokens (JWT).
- `python-decouple`: organize configuration settings, especially secrets (e.g. `.env`), outside the source code.

## Resources
- [Quickly Authenticate Users with FastAPI and Token Authentication](https://www.youtube.com/watch?v=5GxQ1rLTwaU&ab_channel=AkamaiDeveloper)
- [How to Create a FastAPI & React Project - Python Backend + React Frontend](https://www.youtube.com/watch?v=aSdVU9-SxH4&ab_channel=TechWithTim)
- [Building a React Login Page Template](https://clerk.com/blog/building-a-react-login-page-template)
- [Creating a React Frontend for an AI Chatbot](https://medium.com/@codeawake/ai-chatbot-frontend-1823b9c78521)
- [Building an AI Chatbot Powered by Your Data](https://medium.com/@codeawake/ai-chatbot-5bd2fa3324e3)