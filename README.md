# FastAPI + React

## Table of Contents
- [Backend - FastAPI](#backend---fastapi)
- [Frontend - React](#frontend---react)
- React Tutorial
	- [React核心语法]()
	- [React Component通信与插槽]()

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

### 3. Start Backend server
```linux
$ python main.py 
```

## Frontend - React
### 1. Set Up React Project
```linux
# check Node.js version
node -v

# check npm version
npm -v

# upgrade npm
sudo npm install -g npm@latest

# Use Vite (like Django in Python) to create a React project, it will create a package.json file under /frontend
npm create vite@latest frontend --template react
 > Select a framework: React
 > Select a variant: JavaScript

cd frontend

# install all dependencies listed in package.json; create package-lock.json
npm install

# install Axios and add this depencency to package.json
npm install axios

npm install react-router-dom
```
### 2. Write Code
Go to `/frontend/src`:
1. create and edit `api.js` `api.js`
2. create `/contexts`:
    - create and edit `AuthContext.jsx`
3. create `/components`:
    - create and edit `Login.jsx`
    - create and edit `Register.jsx`
    - create and edit `UserProfile.jsx`
4. edit `App.jsx`
### 3. Start Frontend Server
```linux
frontend $ npm run dev
```




## Resources
- [Quickly Authenticate Users with FastAPI and Token Authentication](https://www.youtube.com/watch?v=5GxQ1rLTwaU&ab_channel=AkamaiDeveloper)
- [How to Create a FastAPI & React Project - Python Backend + React Frontend](https://www.youtube.com/watch?v=aSdVU9-SxH4&ab_channel=TechWithTim)
- [Building a React Login Page Template](https://clerk.com/blog/building-a-react-login-page-template)
- [Creating a React Frontend for an AI Chatbot](https://medium.com/@codeawake/ai-chatbot-frontend-1823b9c78521)
- [Building an AI Chatbot Powered by Your Data](https://medium.com/@codeawake/ai-chatbot-5bd2fa3324e3)
- [full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template/tree/master)

## UML Sequence Diagram - Backend
![mermaid-diagram-2024-12-09-151515](https://github.com/user-attachments/assets/265125cf-43a1-47b2-bf67-177d53b004d0)


## UML Sequence Diagram - Frontend
![mermaid-diagram-2024-12-10-175621](https://github.com/user-attachments/assets/867ab168-c5ca-422c-bfb2-3154d0b9a086)

