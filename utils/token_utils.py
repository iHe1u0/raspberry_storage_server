import hashlib
from datetime import datetime, timedelta

# 存储用户和密码的字典
users = {
    "kt": "1109"  # 默认用户名kt,密码1109
}

# 存储 token 的字典
tokens = {}


def get_token(user: str, password: str, timestamp: int) -> str:
    if user not in users or users[user] != password:
        return "Invalid credentials"

    token_str = f"{user}{password}{timestamp}"
    token = hashlib.sha256(token_str.encode()).hexdigest()

    # 生成当前时间和 30 天后的时间
    now = datetime.utcnow()
    expiration_date = now + timedelta(days=30)

    # 存储 token 和其到期时间
    tokens[token] = expiration_date
    return token


def encode(v):
    return hashlib.sha256(v.encode()).hexdigest()
