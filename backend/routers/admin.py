from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

from database import get_db
from models import Admin

router      = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 生成配置 
SECRET_KEY  = "change_this_to_a_random_string_before_deploy"
ALGORITHM   = "HS256"
TOKEN_EXPIRE_HOURS = 16

# 请求体的数据规范
class LoginBody(BaseModel):
    username:   str
    password:   str


def create_token(username: str) -> str:
    # datetime.datetime(2026, 4, 23, 11, 33, 48, 261688)
    expire = datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRE_HOURS)

    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)



# ── POST /api/admin/login
@router.post("/login")
def login(body: LoginBody, db: Session = Depends(get_db)):

    admin = db.query(Admin).filter(Admin.username == body.username).first()
    
    if not admin or not pwd_context.verify(body.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    token = create_token(admin.username)

    return {
        "message"   :  "登录成功",
        "token"     :   token,
        "usernmae"  :   admin.username,
    }

# ── GET /api/admin/verify  ────────────────────────────────
# 前端刷新页面时用来验证 token 是否还有效
@router.get("/verify")
def verify_token(token: str, db: Session = Depends(get_db)):
    
    try:
        # 1. token 不是标准格式 -> 报错
        # 2. 满足标准格式，jwt.encode 就能提取 到 sub 和 exp
        # 3. 自动判断 token exp 状态
        # 4. 下一步手动验证是否是验证的用户
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get('sub')

        admin = db.query(Admin).filter(Admin.username == username).first()        
        if not admin:
            raise HTTPException(status_code=401, detail="Token 无效")

        return {"valide": True, "username": username}
    
    except Exception:
        raise HTTPException(status_code=401, detail="Token 已过期或无效")
