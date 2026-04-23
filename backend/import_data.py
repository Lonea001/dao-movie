import json
import os
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, Movie, Admin

# ── 配置区 ──────────────────────────────────────────────
DATA_FILE       =   "data/samples.json"
ADMIN_USER      =   "admin"
ADMIN_PASS      =   "admin5615"
MAX_IMPORT      =   1000
# ────────────────────────────────────────────────────────

# 加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def clean_str_list(lst: list) -> str:

    # [a, b, "1", 56] -> ["a", "b", "56"] -> "a,b,56"  
    return ",".join([str(x).strip() for x in lst if x])                   

def parse_movie(raw: dict) -> dict | None:
    """ json -> database field """

    rating_info     = raw.get("rating", {})
    rating_avg      = float(rating_info.get("average", 0) or 0)
    rating_count    = int(rating_info.get("rating_people", 0) or 0)

    directors       = [d.get("name", "") for d in raw.get("directors", [])]
    casts           = [c.get("name", "") for c in raw.get("casts", [])[:5]]

    data = {
        "douban_id"     :   str(raw.get("_id", "")),
        "title"         :   raw.get("title", ""),
        "year"          :   str(raw.get("year", "")),
        "rating_ratio"  :   clean_str_list(rating_info.get("stars", [])),           # 电影打分比例，占比。未添加数据库字段
        "rating"        :   rating_avg,                                             # 评分
        "rating_count"  :   rating_count,
        "duration"      :   str(raw.get("duration", "")),
        "summary"       :   raw.get("summary", "").strip(),
        "poster"        :   raw.get("poster", "").strip(),
        "imdb"          :   raw.get("imdb", "").strip(),
        "genres"        :   clean_str_list(raw.get("genres", [])),
        "directors"     :   clean_str_list(directors),
        "casts"         :   clean_str_list(casts),
        "countries"     :   clean_str_list(raw.get("countries", [])),
        "languages"     :   clean_str_list(raw.get("languages", [])),
        "pubdate"       :   clean_str_list(raw.get("pubdate", [])),         # 多个上映日期

    }
    
    return data
        
    
def create_tables():
    print("📦 创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("✅ 建表完成")


def import_movies(db: Session):
    if not os.path.exists(DATA_FILE):
        print(f"    找不到数据集：{DATA_FILE}")
        print(" 将数据文件放到 data/samples.json")
        return
    
    existing = db.query(Movie).count()
    if existing > 0:
        print(f"数据库已有 {existing} 条电影数据，请先跳过导入")
        print(" 如要重新导入，请先删除 movies.db，并重新运行脚本")
        return
    
    print(f"    读取数据文件：{DATA_FILE}")

    movies_to_add = []
    skipped = 0
    count = 0

    # 读取和处理数据集
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            
            try:
                raw = json.loads(line.rstrip(","))
            except json.JSONDecodeError:
                skipped += 1
                continue

            parsed = parse_movie(raw)
            if not parsed or not parsed["title"]:
                skipped += 1
                continue
            
            # 调用数据初始化模型，添加到集合中
            movies_to_add.append(Movie(**parsed))
            count += 1

            if MAX_IMPORT and count >= MAX_IMPORT:
                print(f"    以达到最大导入数量限制：{MAX_IMPORT} 条")
                break
        
    if not movies_to_add:
        print(" 没有可导入的数据，检查文件")
        return
    
    print(f"    共解析{count} 条，跳过 {skipped} 条")
    print("💾  写入数据库中...")

    # 分批导入数据库
    batch_size = 100
    for i in range(0, len(movies_to_add), batch_size):
        batch = movies_to_add[i : i + batch_size]
        db.add_all(batch)
        db.commit()

        print(f"    已写入 {min(i+batch_size, len(movies_to_add))} / {len(movies_to_add)}")

    print(f"✅  电影数据导入完成，共 {len(movies_to_add)}")

def create_admin(db: Session):
    existing = db.query(Admin).filter(Admin.username == ADMIN_USER).first()

    if existing:
        print(f"    管理员 '{ADMIN_USER} 已存在，跳过创建'")
        return
    
    hashed = pwd_context.hash(ADMIN_PASS)
    admin = Admin(username=ADMIN_USER, password_hash=hashed)
    db.add(admin)
    db.commit()

    print(f"    管理员账号创建完成")
    print(f"    用户名：{ADMIN_USER}")
    print(f"    密码： {ADMIN_PASS}")
    print(f"    哈希值：{hashed}")

def main():
    print("=" * 50)
    print("     电影数据库导入脚本")
    print("=" * 50)
    
    create_tables()

    db = SessionLocal()
    try:
        import_movies(db)
        create_admin(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()