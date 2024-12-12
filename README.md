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

### 3. Start Backend server
```linux
$ python main.py 
```

## Frontend - React
### 1. Set Up React Project
```linux
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

### [Tutorial](https://www.bilibili.com/video/BV1xM41197cZ?spm_id_from=333.788.player.switch&vd_source=0c02ef6f6e7a2b0959d7dd28e9e49da4)
1. 创建React项目
	1. 方式一：引入核心文件 e.g. `react.js`
	2. 方式二：使用脚手架 (Scaffold = basic structure/boiler template)
		- Use Create React App `$ npx create-react-app <project-name>`
		- Use Vite `$ npm create vite@latest <project-name> --template react`
		- `cd <project-name>`
		- `npm start // start the app`
	3. 入口文件: index.js / main.jsx
	4  根组件: App.js / App.jsx
	5. React组件的两种创建方式: 函数组件，类组件
	6. 现在主推函数组件
2. JSX = html + javascript
	1. 函数组件return后面的小括号
	2. JSX只能返回一个根元素: e.g. 只能有一个 `<div></div>`
		- 方式2: 使用JSX提供的空标签包括所有 `<> … </>`
	3. 单标签，双标签都需要正确闭合: `<App />`, `<Router></Router>`
3. 数据渲染
	1. 插值功能
		1. 类似python的fstring用法: `{variable}` to access in html
		2. 插值的使用位置：1. 标签内容 `<div>{var}</div>`，2. 标签属性 `<div title={var}>…</div>`
	3. 条件渲染
	4. 列表渲染: 
		- list
		- map (更常用，因为具有有返回值，相比于forEach). 每个element必须要有一个unique key (id)属性
		- 循环生成时 (遍历list, map), 有可能涉及存在多个根标签情况，处理方式是import Fragment，并由`<Fragment></Fragment>`包裹多标签
4. 事件处理
	1. 加一个事件：在标签内部用onClick的方式 `<button onClick={事件处理程序名/eg. handleClick}></button>`
	2. JSX里属性名称使用驼峰命名法
	3. 获取事件的相关信息, 加入参数e: function handleClick(e) {…} e包含了鼠标相关的坐标等信息
5. useState状态处理 
	1. 函数组件默认没有状态
	2. 什么是状态？一个变量(const var = …)一旦赋值，则不可更改。解决办法，将变量转换成userState(var)
	3. `useState` 是React提供的一个函数
		- `const [getContent, setContent] = useState(‘blahblah’)`
		- getContent读取内容，setContent复写内容
	4. 对象形式的状态
		```
        const [data, setData] = useState({
			title: ‘X’,
			content: ‘Y’
			})
        ```
		- 读操作: `data.title`, `data.content`
		- 写操作: 
        ```
        setData({
			title: ‘a’,
			content: ‘Y’
			}) // 所有fields都要重新写一遍
        ```
		- 简便写操作: 
        ```
        setData({
			…data,
			title: ‘a’
			}) //只修改title，注意：要更改的field只能写在最后
        ```
	5. 数组形式的状态
		- `…data`可以在新增元素的后面或者前面，新增元素更新位置会不同
		- `data.filter()` 过滤不需要渲染的元素


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

