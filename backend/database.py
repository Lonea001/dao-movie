from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# sql database saved file-path
DATABASE_URL = "sqlite:///./movies.db"

engine = create_engine(
    DATABASE_URL,
    # 关闭多线程检查，允许多个线程使用同一个数据库连接
    connect_args={"check_same_thread": False}       

)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()           # 模型基类

# FastAPI 调用数据库接口
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

