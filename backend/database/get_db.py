'''
@Project ：PredictDemo 
@File    ：get_db.py
@IDE     ：PyCharm 
@Author  ：Gaogz
@Date    ：2024/10/15 09:36 
@Desc    ：
'''
from .database import Base,engine
from loguru import logger
from .session import SessionLocal
def get_db_pro():
    """
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接
    :return:
    """
    current_db = SessionLocal()
    try:
        yield current_db
    finally:
        current_db.close()


async def init_create_table():
    """
    应用启动时初始化数据库连接
    :return:
    """
    logger.info("初始化数据库连接...")
    Base.metadata.create_all(bind=engine)
    logger.info("数据库连接成功")


get_db = get_db_pro