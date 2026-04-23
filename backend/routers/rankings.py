from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from database import get_db
from models import Ranking, RankingItem, Movie
from routers.movies import movie_to_dict

router = APIRouter()


# ── BaseModel 是 Pydantic 的数据模型基类。
# 用作：专门用来定义数据，长什么样
# 约束请求数据格式。前端少传字段或者类型不对，FastAPI 会自动报错
# 识别请求模型：装数据    检查字段    检查类型    
# 格式和 Ranking 对象匹配。规范请求模型的数据格式
# BaseModel -> RankingCreate
# http request -> RankingCreate -> BaseModel
class RankingCreate(BaseModel):
    name            : str
    description     : Optional[str] = ""
    cover           : Optional[str] = ""
    movie_ids       : List[int]     = []        # 按顺序排列的电影 id 列表


# ── GET /api/rankings/ ─────────────────────────
# 获取所有电影榜单，不含电影列表，只返回基本信息
@router.get("")
def get_rankings(db: Session = Depends(get_db)):

    rankings = db.query(Ranking).order_by(Ranking.created_at.desc()).all()
    result = []
    for r in rankings:
        data = {
            "id"            : r.id,
            "name"          : r.name,
            "description"   : r.description,
            "cover"         : r.cover,
            # 榜单里的所有电影数
            "movie_count"   : len(r.items),
            "created_at"    : r.created_at,
        }
        result.append(data)

    return {"items": result}


# ── GET /api/rankings/{ranking_id} ────────────────────────
# 获取 单个榜单 详情
@router.get("/{ranking_id}")
def get_ranking(ranking_id: int, db: Session = Depends(get_db)):
    
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()
    
    if not ranking:
        raise HTTPException(status_code=404, detail="榜单不存在")

    movies = []
    for item in ranking.items:
        movie = db.query(Movie).filter(Movie.id == item.movie_id).first()
        if movie:
            d = movie_to_dict(movie)
            d['rank_order'] = item.rank_order
            movies.append(d)

    ranking_data = {
        "id"            : ranking.id,
        "name"          : ranking.name,
        "description"   : ranking.description,
        "cover"         : ranking.cover,
        "created_at"    : ranking.created_at,
        "movies"        : movies,
    }

    return ranking_data

# ── POST /api/ranking ────────────────────────────────────────────
# 创建榜单，仅限管理员
@router.post("")
def create_ranking(body: RankingCreate, db: Session = Depends(get_db)):
    
    # 1. 根据 请求体榜单数据 去创建 Ranking 数据库对象
    ranking = Ranking(                           # 创建 Ranking 对象
        name            = body.name,
        description     = body.description,
        cover           = body.cover,
    )

    db.add(ranking)
    db.commit()
    db.refresh(ranking)                         # 得到第二部分：生成的 id 和 created_at

    # 2. 为创建好的初始榜单，添加所属数据
    # pydantic -> body 是 Ranking 规范 -> movie_ids 就是所给的电影排名顺序和编号 
    for order, m_id in enumerate(body.movie_ids, start=1):
        item = RankingItem(
            ranking_id  = ranking.id,
            movie_id    = m_id,
            rank_order  = order,
        )
        db.add(item)

    db.commit()

    return {"message": "榜单创建成功", "id": ranking.id}

# ── PUT /api/rankings/{ranking_id} ────────────────────────────────
# 更新榜单
@router.put("/{ranking_id}")
def update_ranking(ranking_id: int, body: RankingCreate, db: Session = Depends(get_db)):
    """ 根据请求，更改对应 ranking_id 榜单 """

    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()

    if not ranking:
        raise HTTPException(status_code=404, detail="榜单不存在")

    # 1. 修改表单 外部信息
    ranking.name        = body.name
    ranking.description = body.description
    ranking.cover       = body.cover

    # 2. 先删除 榜单下所有的电影
    db.query(RankingItem).filter(RankingItem.ranking_id == ranking_id).delete()
    # 再重新添加
    for order, m_id in enumerate(body.movie_ids, start=1):
        item = RankingItem(
            ranking_id      = ranking_id,
            movie_id        = m_id,
            rank_order      = order,
        )
        db.add(item)
    db.commit()

    return {"message": "榜单更新成功"}


# DELETE /api/rankings/{ranking_id}
# 删除榜单
@router.delete("/{ranking_id}")
def delete_ranking(ranking_id: int, db: Session = Depends(get_db)):
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()

    if not ranking:
        raise HTTPException(status_code=404, detail="榜单不存在")

    db.delete(ranking)
    db.commit()

    return {"message": "榜单已删除"}