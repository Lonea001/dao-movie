from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Interaction, Movie

router = APIRouter()

def _toggle(movie_id: int, action: str, db: Session) -> dict:
    """ 点赞/收藏，互相切换。有则取消，无则添加 (toggle 逻辑)"""

    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="电影不存在")

    existing = db.query(Interaction).filter(
        Interaction.movie_id    == movie_id,
        Interaction.type        == action,
    ).first()

    # 如果已有点赞，取消点赞
    if existing:
        db.delete(existing)
        db.commit()
        status = "cancelled"

    else:
        # 一条互动数据
        data = Interaction(
            movie_id    = movie_id,
            type        = action,
        )
        db.add(data)
        db.commit()
        status = "added"

    # 返回这部电影的总互动数
    count = db.query(Interaction).filter(
        Interaction.movie_id    == movie_id,
        Interaction.type        == action,
    ).count()

    return {"status": status, "count": count}


# ── POST /api/interaction/{movie_id}/like
@router.post("/{movie_id}/like")
def toggle_like(movie_id: int, db: Session = Depends(get_db)):
    return _toggle(movie_id, "like", db)


# ── POST /api/interaction/{movie_id}/collect
@router.post("/{movie_id}/collect")
def toggle_collect(movie_id: int, db: Session = Depends(get_db)):
    return _toggle(movie_id, "collect", db)


# ── GET /api/interaction/{movie_id}/status
@router.get("/{movie_id}/status")
def get_status(movie_id: int, db: Session = Depends(get_db)):
    like_count      = db.query(Interaction).filter(
        Interaction.movie_id == movie_id,
        Interaction.type     == "like"
    ).count()

    collect_count   = db.query(Interaction).filter(
        Interaction.movie_id    == movie_id,
        Interaction.type        == "collect"
    ).count()

    return {
        "like_count":       like_count,
        "collect_count":    collect_count
    }