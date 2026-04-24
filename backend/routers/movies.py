from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from database import get_db
from models import Movie, Interaction

router = APIRouter()

def movie_to_dict(movie: Movie, db: Session = None) -> dict:
    """把 Movie 对象转成前端所需的字典格式"""

    # 传了 db 才去找 点赞数和收藏数
    like_count      = 0
    collect_count   = 0
    if db:
        like_count = db.query(Interaction).filter(Interaction.movie_id == movie.id,
                                                  Interaction.type == "like").count()
        collect_count = db.query(Interaction).filter(Interaction.movie_id == movie.id,
                                                     Interaction.type == "collect").count()
    data = {
        "id"            : movie.id,
        "douban_id"     : movie.douban_id,
        "title"         : movie.title,
        "year"          : movie.year,
        "rating_ratio"  : movie.rating_ratio,
        "rating"        : movie.rating,
        "rating_count"  : movie.rating_count,
        "duration"      : movie.duration,
        "summary"       : movie.summary,
        "poster"        : movie.poster,
        "imdb"          : movie.imdb,
        "genres"        : movie.genres.split(',') if movie.genres else [],
        "directors"     : movie.directors.split(',') if movie.directors else [],
        "casts"         : movie.casts.split(',') if movie.casts else [],
        "countries"     : movie.countries.split(',') if movie.countries else [],
        "languages"     : movie.languages.split(',') if movie.languages else [],
        "pubdate"       : movie.pubdate.split(',') if movie.pubdate else [],
        "like_count"    : like_count,
        "collect_count" : collect_count,
    }

    return data

# ── GET /api/movies ────────────────────────────────────────────────
# 电影列表接口
# 支持：
#       分页
#       关键词搜索
#       类型筛选
#       年份筛选
#       排序

@router.get("")
def get_movies(
        page        : int           = Query(1,  ge=1,           description="页码, 从1开始"),
        page_size   : int           = Query(24, ge=1, le=100,   description="每页数量"),
        q           : Optional[str] = Query(None,               description="搜索关键词 （片名 / 导演 / 演员）"),
        genre       : Optional[str] = Query(None,               description="类型筛选，如：科幻"),
        year        : Optional[str] = Query(None,               description="年份筛选，如：2016"),
        sort_by     : str           = Query("rating",           description="排序：rating / year / rating_count"),
        db          : Session       = Depends(get_db)
    ):
    # db 查询 Movie 表
    query = db.query(Movie)

    # 1. 关键字筛选：匹配片名、导演、演员
    if q:
        keyword = f"%{q}%"                          # "%q%"     %: 数据库任意字符；包含 q 的所有内容
        query = query.filter(
            or_(
                Movie.title.like(keyword),
                Movie.directors.like(keyword),
                Movie.casts.like(keyword)
            )
        )
    
    # 2. 类型筛选  genres 是逗号字符串
    if genre:
        query = query.filter(Movie.genres.like(f"%{genre}%"))

    # 3. 年份筛选
    if year:
        query = query.filter(Movie.year == year)

    sort_map = {
        "rating"        : Movie.rating.desc(),       # descend 降序  ascend 升序
        "year"          : Movie.year.desc(),
        "rating_count"  : Movie.rating_count.desc()
    }
    query = query.order_by(sort_map.get(sort_by, Movie.rating.desc()))

    # 总数 （前端分页使用）
    total = query.count()
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()

    query_data = {
        "total"     : total,
        "page"      : page,
        "page_size" : page_size,
        "pages"     : (total + page_size - 1) // page_size,      # 向上取整公式，为余数多创造一页。-1 影响多进位
        "items"     : [movie_to_dict(m, db) for m in items]
    }
    return query_data


# ── GET /api/movies/genres ────────────────────────────────────────
# 获取所有电影类别，前端筛选标签用

@router.get("/genres")
def get_genres(db: Session = Depends(get_db)):

    rows = db.query(Movie.genres).all()
    genre_set = set()

    # db.query -> genres -> [("喜剧",), ("科幻"), ]
    # (genre_str,) -> 表示元组     genre_str = "喜剧,科幻,动作" 
    for (genre_str,) in rows:
        if genre_str:
            for g in genre_str.split(','):
                g = g.strip()
                if g:
                    genre_set.add(g)

    return {"genres": sorted(list(genre_set))}

# ── GET /api/movies/top ────────────────────────────────────

@router.get("/top")
def get_top_movies(
    limit: int = Query(10, ge=1, le=100),
    db   : Session = Depends(get_db)
    ):

    items = (
        db.query(Movie)
        .filter(Movie.rating > 0)
        .order_by(Movie.rating.desc())
        .limit(limit)
        .all()
    )

    return {"items": [movie_to_dict(m) for m in items]}

# ── GET /api/movies/{movie_id} ────────────────────────────────────
# 电影详情，含点赞、收藏

@router.get("/{movie_id}")
def get_movie(movie_id: int, db: Session = Depends(get_db)):

    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="电影不存在")

    return movie_to_dict(movie, db)