'''
@Project ：PredictDemo 
@File    ：models.py
@IDE     ：PyCharm 
@Author  ：Gaogz
@Date    ：2024/10/15 09:48 
@Desc    ：
'''
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,Float
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('CURRENT_TIMESTAMP'))

class Post(Base):
    __tablename__ = 'posts'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    #owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    #owner = relationship("User") # referencing to User class below,
    # owner will be used from retreaving information about the post owner

class StocksModel(Base):
    __tablename__ = 'Stocks'
    __table_args__ = {'extend_existing': True}

    id = Column(String, primary_key=True, nullable=False,comment="id")
    code = Column(String, nullable=False, comment="股票代码")
    date = Column(String, nullable=False,comment="日期")
    open = Column(Float, nullable=False,comment="开盘价")
    close = Column(Float, nullable=False,comment="收盘价")
    adj_close = Column(Float, nullable=False,comment="调整收盘价")
    high = Column(Float, nullable=False,comment="最高价")
    low = Column(Float, nullable=False,comment="最低价")
    volume = Column(Integer, nullable=False,comment="成交量")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'),comment="创建时间")
    status = Column(Integer, nullable=False,default=1,comment="状态") # 1:正常，2：删除
