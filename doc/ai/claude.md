### 🔌 核心 API 接口

| 接口                                     | 说明               |
| ---------------------------------------- | ------------------ |
| `GET /movies?page=1&q=关键词&genre=科幻` | 搜索+分类列表      |
| `GET /movies/{id}`                       | 电影详情           |
| `GET /genres`                            | 获取所有类型       |
| `GET /rankings`                          | 榜单列表           |
| `GET /rankings/{id}`                     | 榜单详情（含电影） |
| `POST /movies/{id}/like`                 | 点赞               |
| `POST /movies/{id}/collect`              | 收藏               |
| `POST /admin/login`                      | 管理员登录         |
| `POST /admin/rankings`                   | 创建/编辑榜单      |



### 结构

```
movie-site/
│
├── backend/                    # Python + FastAPI
│   ├── main.py                 # 入口，注册路由、启动配置
│   ├── database.py             # SQLite 连接、Session 管理
│   ├── models.py               # 数据库表结构（SQLAlchemy）
│   ├── schemas.py              # 接口数据格式（Pydantic）
│   │
│   ├── routers/                # 按功能拆分接口
│   │   ├── movies.py           # 列表、搜索、详情、分类
│   │   ├── rankings.py         # 榜单增删改查
│   │   ├── interaction.py      # 点赞、收藏
│   │   └── admin.py            # 登录、后台管理
│   │
│   ├── utils/
│   │   └── auth.py             # JWT 登录鉴权
│   │
│   ├── data/
│   │   └── movies.csv          # 原始数据文件放这里
│   │
│   ├── import_data.py          # 一次性数据导入脚本
│   ├── movies.db               # SQLite 数据库文件
│   └── requirements.txt        # 依赖列表
│
├── frontend/                   # Vue 3 + Vite
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   │
│   │   ├── api/                # 所有请求封装在这里
│   │   │   ├── request.js      # Axios 实例、拦截器
│   │   │   ├── movies.js       # 电影相关请求
│   │   │   └── rankings.js     # 榜单相关请求
│   │   │
│   │   ├── views/              # 页面
│   │   │   ├── Home.vue        # 首页（轮播+推荐+榜单入口）
│   │   │   ├── MovieList.vue   # 电影列表（搜索+分类筛选）
│   │   │   ├── MovieDetail.vue # 电影详情
│   │   │   ├── Rankings.vue    # 榜单列表
│   │   │   ├── RankingDetail.vue # 单个榜单详情
│   │   │   └── Admin.vue       # 管理后台
│   │   │
│   │   ├── components/         # 可复用组件
│   │   │   ├── MovieCard.vue   # 电影卡片（列表里用）
│   │   │   ├── SearchBar.vue   # 搜索框
│   │   │   ├── GenreFilter.vue # 类型筛选标签
│   │   │   └── Navbar.vue      # 顶部导航
│   │   │
│   │   ├── router/
│   │   │   └── index.js        # 路由配置
│   │   │
│   │   └── stores/             # Pinia 状态管理
│   │       └── user.js         # 管理员登录状态
│   │
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── nginx.conf                  # 部署时 Nginx 配置
└── README.md
```





### 步骤

Step 1 — 本地建好项目结构

```
mkdir movie-site && cd movie-site
mkdir backend frontend
cd backend
python3 -m venv venv          # 创建虚拟环境
source venv/bin/activate      # Mac/Linux
# venv\Scripts\activate       # Windows

pip install fastapi uvicorn sqlalchemy pydantic python-jose passlib pandas
pip freeze > requirements.txt
```



Step 3 — 写核心代码（我可以帮你生成）

顺序是：

1. `database.py` → 数据库连接
2. `models.py` → 建表
3. `import_data.py` → 导入 CSV
4. `schemas.py` → 接口格式
5. `routers/movies.py` → 查询接口
6. `main.py` → 启动





#### 第二阶段：前端开发 （本地）

bash

```bash
cd ../frontend
npm create vue@latest .    # 选 Vue3 + Vue Router + Pinia
npm install
npm install element-plus axios
```

然后按顺序写页面：

1. `MovieList.vue` — 列表+搜索
2. `MovieDetail.vue` — 详情
3. `Rankings.vue` — 榜单
4. `Admin.vue` — 后台





1. git push 代码到 GitHub
2. 服务器上 git clone 下来
3. 服务器安装依赖、跑后端
4. 前端 npm run build 生成静态文件
5. 配置 Nginx 指向前端文件 + 反向代理后端