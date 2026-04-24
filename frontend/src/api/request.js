import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建 axios 示例，封装请求
const request = axios.create({
    baseURL: '/api',
    timeout: 10000,
})

// 拦截器：请求发送之前，封装 请求内容
// interceptors 拦截器系统
// axios - interceptors - request 请求拦截器  / response 响应拦截器
// use()    注册一个拦截规则
// config   请求的配置信息 config {url: ', method: '', headers: '',}
// 给 headers 请求头 添加一个认证请求字段 Authorization
// Bearer 标准写法
// return config 把修改后的请求配置返回给 axios，正常发送

request.interceptors.request.use( config => {
    const token = localStorage.getItem('admin_token')
    if (token) {
        // 添加认证字段
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})


// 创建响应式拦截：统一处理错误
// 每次接口返回结果，先经过这里
// use -> (成功请求，失败请求)
// 请求成功时，res 是 axios 返回的整个响应对象 直接得到 data
// 有 err 时，统一弹出错误提示
// err 错误响应对象     ?. 可选链操作符，防止类型报错   || 兜底报错内容
// Elment-plus  -> Elmessage
// return 把错误结果抛给 调用代码       Promise 调用原型    reject 失败了的结果

request.interceptors.response.use(
    res => res.data,
    err => {
        const msg = err.response?.data?.detail || "网络错误，稍后重试"
        ElMessage.error(msg)
        return Promise.reject(err)
    }
)

export default request