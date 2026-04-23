from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import Base

# 导入 api 路由
from routers import movies, rankings, interaction, admin

# 启动时自动建表，存在则跳过
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="大盗影视",
    description="毕设 —— 数据展示平台",
    version="0.0.1",
)

# ── 跨域配置 ──────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# ── 注册路由 ─────────────────────────────
app.include_router(movies.router,           prefix="/api/movies",       tags=["电影"])
app.include_router(rankings.router,         prefix="/api/rankings",     tags=["榜单"])
app.include_router(interaction.router,      prefix="/api/interaction",  tags=["点赞/收藏"])
app.include_router(admin.router,            prefix="/api/admin",        tags=["管理员"])

@app.get("/")
def root():
    return {
        "message": "电影网站 API 正在运行",
        "docs"   :  "/docs"
    }