'''
@Project ：PredictDemo 
@File    ：token_utils.py
@IDE     ：PyCharm 
@Author  ：Gaogz
@Date    ：2024/10/15 15:12 
@Desc    ：
'''
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from schema.schemas import TokenData
from database.models import models
from database.get_db import get_db

# 签名部分的秘钥
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# tokenUrl这个参数用来指定进行Oauth2认证接口地址，这里用的是相对路径
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/login') # 'login' is according to login endpointname see in auth.py


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credential_exception

        token_data = TokenData(id=int(id))

    except JWTError:
        raise credential_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f"Could not validate credentials",
                                         headers={"WWW-Authenticate": "Bearer"}
                                         )
    token = verify_access_token(token, credential_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user