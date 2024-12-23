# React Tutorial
## [React核心语法](https://www.bilibili.com/video/BV1pF411m7wV?vd_source=0c02ef6f6e7a2b0959d7dd28e9e49da4)
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

## [React Component通信与插槽](https://www.bilibili.com/video/BV1xM41197cZ?vd_source=0c02ef6f6e7a2b0959d7dd28e9e49da4)
1. 为DOM组件设置Props (属性) e.g. `<img src={image} alt=“xx”/>`中的src, alt
    1. DOM组件Props中的类属性: `className=“small”`
    2. DOM组件Props中的style属性: 
    ```jsx
    style={{
        width: “100vh”,
        height: 200,
        backgroundColor: “grey”
        }} 
    ```
    3. JSX的展开语法: 
将所有属性提前定义在一个对象中.
注: `alt`属性不能提出来提前定义
    ```jsx
    const imgData = {
        className: “small”,
        style: {
        width: “100vh”,
        height: 200,
        backgroundColor: “grey”
        }}
    <img src={image} alt=“” {…imgData} />
    ```
    小贴士：JSX的展开操作(`…`)并不是ES6的展开运算符

    `{…imgData}` 相当于对象shallow copy: `…imgData` -> 将imgData拆解开; `{}` -> 将拆解出来的所有key-value pair放入一个新对象

    但是！`<img  src={image} alt="xyz" {…imgData} />`这里 `{…imgData}`的`{}`只是jsx的语法标记，算是jsx单独的功能支持，编译时会自动有额外处理，不能只解开`…imgData` 却不包裹`{}`

2. React组件的Props
```jsx
function Article(props) {
  return (
    <div>
      <h2>{props.title}</h2>
      <p>{props.content}</p>
    </div>
)
}
// 直接的传入解构写法
function Article({title, content, active}) {
  return (
    <div>
      <h2>{title}</h2>
      <p>{content}</p>
      <p>state: {active ? “on”:”hidden”}</p>
    </div>
)
}
====App()
<Article 
  title="abc"
  content="123"
  active // 如果在此处写了, active=true；如果不写，默认为false
/>

<Article 
  title="xyz"
  content="456"
/>
```
操作步骤：

step 1. 请求功能所需的数据

step 2. 创建Article组件

step 3. 将文章的数据分别传递给Article

2. 在React组件中展开props的使用场景
```jsx
function Detail({content, active}) {
    return (
        <>
        <p>{content}</p>
        <p>state: {active ? “on”:”hidden”}</p>
        </>
    )
}

function Article({title, detailData}) {
    return (
        <div>
        <h2>{title}</h2>
        <Detail {…detailData} />
        </div>
    )
}
=====App()
const articleData = {
    title: ‘abc’,
    detailData: {
        content: ‘content1’,
        active: true // 需要显性赋值
    }
    }

<Article
    {…articleData}
/>
```
3. 将JSX作为props传递(组件插槽)
    ```jsx
    // 预定义一个属性叫做children，接收包裹的整个jsx (<li>..</lis>…)作为props传入
    function List({children}) {
        return (
            <ul>
                {children}
            </ul>
        )
    } 
    ====App
    <List>
        <li>list 1</li>
        <li>list 2</li>
        <li>lits 3</li>
    </List>
    ```
    1. 向多个位置传递JSX
    ```jsx
    function List({children, title, footer=<div>default</div>}) {
        return (
            <>
                <h2>{title}</h2>
                <ul>
                    {children}
                </ul>
                {footer}
            </>
        )
    } 
    ====App
    <List
        title="abc"
        footer={<p>bottom content</p>}
    >
        <li>list 1</li>
        <li>list 2</li>
        <li>lits 3</li>
    </List>
    ```

4. 子组件向父组件传值

从父组件传入子组件的props都是单向的，所以子组件只能做read-only的操作。如果希望子组件向父组件进行数据传递的话，
```jsx
function Detail({ onActive }) { // 接收父组件中定义的func
  const [status, setStatus] = useState(false)
  function handleClick() {
     setStatus(!status)
     onActive(status)
  }
  return (
    <div>
      <p style={{
         display: status ? 'block' : 'none'
       }}>detail content</p>
      <button onClick={handleClick}>submit</button>
    </div>
  )
}
====App
function handleActive(status) {
   console.log(status)
}
<Detail
    onActive={handleActive} // 将 handleActive func当作props传入子组件
/>
```
5. 使用Context进行多级组件传值

`const LevelContext = createContext(1) // global variable`

之后如果在一个子组件中想要access，可以在函数体中写:

`const level = useContext(LevelContext)`