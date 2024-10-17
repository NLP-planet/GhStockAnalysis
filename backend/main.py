import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger
from database.get_db import init_create_table
from api import user,data_load,ai_chat
from config.serverconfig import AppConfig


# 生命周期事件
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时的代码
    logger.info(f"{AppConfig.app_name}开始启动")

    await init_create_table()

    logger.info(f"{AppConfig.app_name}启动成功")
    yield
    logger.info(f"{AppConfig.app_name} is shutting down")



app = FastAPI( title=AppConfig.app_name,
    description=f'{AppConfig.app_name}接口文档',
    version=AppConfig.app_version,
    lifespan=lifespan)


@app.get('/') # this derocator in order the function below do not act like ordinary function, btw this is get http method
def root():
    return {'massage':'hello world!!'}

app.include_router(data_load.router)
app.include_router(ai_chat.router)
app.include_router(user.user_router) # all functionalities about user are in routers directory



if __name__ == '__main__':
    workers = os.getenv("WORKERS",1)

    uvicorn.run(
        app='main:app',
        host=AppConfig.app_host,
        port=AppConfig.app_port,
        reload=True,
        workers=workers
    )