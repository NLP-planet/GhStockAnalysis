'''
@Project ：PredictDemo 
@File    ：serverconfig.py
@IDE     ：PyCharm 
@Author  ：Gaogz
@Date    ：2024/10/15 09:21 
@Desc    ：
'''
import os
from loguru import logger
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pathlib import Path
def get_env(key, default):
    val = os.environ.get(key, "")
    return val or default

def print_parameters(cls):
    attrs = {k:v.default for k,v in cls.__fields__.items()}
    logger.info("Parameters of class 【{}】 are: {}".format(cls.__name__, attrs))
    return cls



ROOT_PATH = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
@print_parameters
class AppSettings(BaseModel):
    """
    应用配置
    """
    app_env:str =get_env("GH_APP_ENV",'dev')
    app_name:str =get_env("GH_APP_NAME","GH-Stock-Analysis")
    app_root_path:str=get_env("GH_APP_ROOT_PATH","") #/text
    app_host:str =get_env("GH_APP_HOST","0.0.0.0")
    app_port:int =get_env("GH_APP_PORT",9001)
    app_version:str=get_env("GH_APP_VERSION","0.1.0")
    app_reload:bool=True
    app_ip_location_query:bool=True
    app_sampe_time_login:bool=True

@print_parameters
class DataBaseSettings(BaseSettings):
    """
    数据库配置
    """
    db_host: str = '127.0.0.1'
    db_port: int = 3306
    db_username: str = 'root'
    db_password: str = 'root123'
    db_database: str = str(ROOT_PATH /'sqlite_db/info.db')
    db_echo: bool = True

AppConfig=AppSettings()
DataBaseConfig=DataBaseSettings()

if __name__=="__main__":

    print(ROOT_PATH)
    print(DataBaseConfig.db_database)