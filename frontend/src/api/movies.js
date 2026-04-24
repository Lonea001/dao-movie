import request from './request'

// 调用后端请求

// 封装 获取电影列表数据的接口
// 并导出给外部使用 export {getMovies}
// () => 定义一个函数
// params 发起请求时，可以传参数
// 函数调用封装的 axios 发送 GET 请求 /api/movies
// { params } 为查询参数 request.get(url, { params: params })
export const getMovies = (params) => request.get('/movies', {params})


// 电影详情
export const getMovie = (id) => request.get(`/movies/${id}`)

// 首页 Top 电影
export const getTopMovies = (limit = 10) => request.get('/movies/top', { params: {limit} })

// 所有电影类型
export const getGenres = () => request.get('/movies/genres')

// 点赞
export const likeMovie = (id) => request.post(`/interaction/${id}/like`)

// 收藏
export const collectMovie = (id) => request.post(`/interaction/${id}/collect`)