'''
@Project ：PredictDemo 
@File    ：database.py
@IDE     ：PyCharm 
@Author  ：Gaogz
@Date    ：2024/10/15 09:34 
@Desc    ：
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.serverconfig import DataBaseConfig

# 创建sqlite连接引擎
#SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db'
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DataBaseConfig.db_database}"

# 创建引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=DataBaseConfig.db_echo)

#创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建一个映射关系基类
Base = declarative_base()
