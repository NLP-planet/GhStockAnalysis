from pydantic import BaseModel, EmailStr,Field # pydantic used for request and respond validation
from datetime import datetime
from typing import Optional

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
        


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int

class TokenData(BaseModel):
    id: Optional[int] = None


class Stock(BaseModel):
    chinese_name: str
    code: str
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    adj_close: float

class StockReq(BaseModel):
    code: str=Field(description="股票代码")
    start_date: str=Field(description="开始时间")
    end_date: str=Field(description="截止时间",default=datetime.now().strftime("%Y-%m-%d"))

class StockReqAll(BaseModel):
    code: str=Field(description="股票代码")

class Chat(BaseModel):
    user_input: str=Field(description="用户问题")
