import re
import time
import httpx
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Movie

SUBJECT_URL = "https://movie.douban.com/subject/{}/"

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "referer": "https://www.bing.com/",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"147\", \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"147\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0"
}
COOKIES = {
    "bid": "aUxLrXi_NbQ",
    "ll": "\"118172\"",
    "_vwo_uuid_v2": "D8CC3FC523AA0EA5DD9BB2BCEC6F98686|dc47ed0133023b51072c5214477ef73f",
    "viewed": "\"1322336_37312585_33442259\"",
    "dbcl2": "\"273505308:ASxQkCeGB9g\"",
    "push_noty_num": "0",
    "push_doumail_num": "0",
    "ck": "SmnO",
    "frodotk_db": "\"4ae1ef6e1627d4cfe0a5ce4a42777e6d\"",
    "ap_v": "0,6.0"
}

def extract_poster(html: str) -> str | None:
    patterns = [
        r'"image"\s*:\s*"([^"]+)"',
        r"'image'\s*:\s*'([^']+)'",
        r'<meta\s+property="og:image"\s+content="([^"]+)"',
        r'"image2"\s*:\s*"([^"]+)"',
        r"'image2'\s*:\s*'([^']+)'",
    ]

    for pattern in patterns:
        m = re.search(pattern, html, re.IGNORECASE)
        if m:
            url = m.group(1).strip()
            if url.startswith("http"):
                return url
    return None

def refresh_one(movie: Movie, client: httpx.Client) -> bool:
    if not movie.douban_id:
        return False
    print(movie.douban_id)
    url = SUBJECT_URL.format(movie.douban_id)
    try: 
        resp = client.get(url, headers={**HEADERS, "Referer": url}, cookies=COOKIES, timeout=15)
        if resp.status_code != 200:
            print(f"[{movie.id}] subject 页面失败: {resp.status_code}")
            return False

        poster = extract_poster(resp.text)
        if not poster:
            print(f"[{movie.id}] 没解析到海报")
            return False

        movie.poster = poster
        print(f"[{movie.id}] 更新成功 -> {poster}")
        return True
    
    except Exception as e:
        print(f"[{movie.id}] 异常: {e}")
        return False

def main():
    db: Session = SessionLocal()
    updated = 0

    try:
        movies = db.query(Movie).filter(Movie.douban_id.isnot(None)).all()

        with httpx.Client(follow_redirects=True) as client:
            for i, movie in enumerate(movies, start=1):
                ok = refresh_one(movie, client)
                if ok:
                    updated += 1
                    db.commit()
                else:
                    db.rollback()

                if i % 20 == 0:
                    print(f"已处理 {i}/{len(movies)}，成功 {updated}")

                time.sleep(0.5)   # 限速，别打太猛

        print(f"完成，成功更新 {updated} 条")
    finally:
        db.close()

if __name__ == "__main__":
    main()