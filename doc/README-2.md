# 大盗影视（Dao-movie）

一个基于 **Vue 3 + Vite + Element Plus** 的电影展示与榜单管理系统前端项目，包含前台浏览与后台榜单管理两部分，适合作为毕业设计中的前后端分离项目。

## 项目简介

本项目面向电影信息展示与榜单管理场景，分为两个主要模块：

- **前台用户端**：提供首页推荐、电影列表、电影详情、榜单列表、榜单详情等功能。
- **后台管理端**：提供管理员登录、榜单新增、编辑、删除以及榜单电影维护等功能。

项目通过 `Vite` 提供开发环境，使用 `Vue Router` 组织页面路由，使用 `axios` 封装接口请求，并通过开发代理将 `/api` 请求转发到后端服务。

## 技术栈

- Vue 3
- Vite
- Vue Router
- Pinia
- Element Plus
- Axios

## 目录结构

```text
Dao-movie/
├─ backend/                  # 后端目录（当前 README 主要说明前端）
└─ frontend/
   ├─ index.html             # 项目入口 HTML
   ├─ vite.config.js         # Vite 配置与代理
   ├─ package.json           # 依赖与脚本
   └─ src/
      ├─ main.js             # 应用入口
      ├─ App.vue             # 根组件
      ├─ router/
      │  └─ index.js         # 路由配置与路由守卫
      ├─ api/
      │  ├─ request.js       # axios 实例与拦截器
      │  ├─ movies.js        # 电影相关接口
      │  ├─ rankings.js      # 榜单相关接口
      │  └─ admin.js         # 管理员相关接口
      ├─ layouts/
      │  ├─ MainLayout.vue   # 前台布局
      │  └─ AdminLayout.vue  # 后台布局
      ├─ components/
      │  └─ MovieCard.vue    # 电影卡片组件
      └─ views/
         ├─ Home.vue         # 首页
         ├─ MovieList.vue    # 电影列表
         ├─ MovieDetail.vue  # 电影详情
         ├─ Rankings.vue     # 榜单列表
         ├─ RankingDetail.vue# 榜单详情
         └─ admin/
            ├─ Login.vue     # 管理员登录页
            └─ AdminHome.vue # 后台管理首页
```

## 已实现功能

### 1. 前台模块

- 首页推荐展示
- Top 电影展示
- 榜单入口展示
- 电影列表分页浏览
- 电影关键字搜索
- 按类型筛选电影
- 按评分、年份、评价人数排序
- 电影详情页展示
- 点赞 / 收藏交互
- 榜单列表浏览
- 榜单详情查看

### 2. 后台模块

- 管理员登录
- 登录状态拦截
- 榜单列表管理
- 新增榜单
- 编辑榜单
- 删除榜单
- 为榜单添加电影
- 退出登录

## 路由说明

### 前台路由

- `/`：首页
- `/movies`：电影列表
- `/movies/:id`：电影详情
- `/rankings`：榜单列表
- `/rankings/:id`：榜单详情

### 后台路由

- `/admin`：管理员登录页
- `/admin/home`：后台首页（需要登录）

后台页面通过路由守卫判断是否存在 `admin_token`，未登录时会跳转回 `/admin`。

## 接口说明

项目当前前端已经封装以下接口模块：

### 电影相关接口

- `getMovies(params)`：获取电影列表
- `getMovie(id)`：获取电影详情
- `getTopMovies(limit)`：获取首页 Top 电影
- `getGenres()`：获取电影类型列表
- `likeMovie(id)`：点赞电影
- `collectMovie(id)`：收藏电影

### 榜单相关接口

- `getRankings()`：获取榜单列表
- `getRanking(id)`：获取榜单详情
- `createRanking(data)`：创建榜单
- `updateRanking(id, data)`：更新榜单
- `deleteRanking(id)`：删除榜单

### 管理员相关接口

- `login(data)`：管理员登录
- `verifyToken(token)`：校验 token（已定义，可继续接入登录校验流程）

## 开发环境运行

### 1. 进入前端目录

```bash
cd frontend
```

### 2. 安装依赖

```bash
npm install
```

### 3. 启动开发服务器

```bash
npm run dev
```

启动后按终端提示访问本地开发地址。

## 开发代理配置

项目在 `vite.config.js` 中配置了开发代理：

```js
server: {
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
    }
  }
}
```

这表示前端开发环境中的 `/api` 请求会被转发到本地后端服务，用于解决跨域问题。

## 登录与鉴权说明

- 管理员登录成功后，会将 `token` 保存到 `localStorage` 中。
- axios 请求拦截器会自动把 token 放到请求头中的 `Authorization` 字段。
- 路由守卫会对需要登录的后台页面进行拦截。

## 当前项目特点

- 前后台分离结构清晰
- 前台浏览链路完整
- 后台管理链路已具备基础闭环
- API 分层清晰，便于后续扩展
- 适合继续完善为毕业设计答辩项目

## 后续可优化方向

- 完善异常处理与空状态展示
- 接入 `verifyToken` 做 token 有效性校验
- 增加表单校验与操作反馈
- 优化页面视觉样式与响应式布局
- 补充单元测试或接口联调说明
- 完善部署文档

## 常见问题

### 1. `npm run dev` 报找不到 `package.json`

请确认当前目录在 `frontend` 下执行，而不是项目外层目录。

```bash
cd frontend
npm run dev
```

### 2. Vite 提示找不到 `pinia`

说明依赖未安装，可执行：

```bash
npm install pinia
```

### 3. 页面空白或接口异常

请检查：

- 前端依赖是否安装完整
- 后端服务是否已在 `127.0.0.1:8000` 启动
- `request.js` 中 Element Plus 消息组件导入是否正确
- 浏览器控制台是否有报错信息

## 项目说明

本项目适合作为电影信息展示与后台管理方向的课程设计或毕业设计前端部分。当前主流程已经搭建完成，后续可继续进行后端联调、界面优化、异常处理与部署完善。

## 许可证

仅用于学习、课程设计与毕业设计交流。