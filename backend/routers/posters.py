from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import httpx

from database import get_db
from models import Movie

router = APIRouter()

@router.get("/{movie_id}")
async def get_poster(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie or not movie.poster:
        raise HTTPException(status_code=404, detail="海报不存在")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Referer": f"https://movie.douban.com/subject/{movie.douban_id}/",
        "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    }

    async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
        resp = await client.get(movie.poster, headers=headers)

    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail=f"海报拉取失败: {resp.status_code}")

    return StreamingResponse(
        iter([resp.content]),
        media_type=resp.headers.get("content-type", "image/jpeg"),
        headers={"Cache-Control": "public, max-age=86400"}
    )