'''
@Project ：GhStockAnalysis 
@File    ：dataload_server.py
@IDE     ：PyCharm 
@Author  ：Gaogz
@Date    ：2024/10/16 10:43 
@Desc    ：
'''
import uuid
import pandas as pd
from config.serverconfig import ROOT_PATH
from utils.data_utils import download_stock_data,download_stock_all_data
from database.models.models import StocksModel
from database.crud import stocks_crud
from loguru import logger

stock_code_cn = pd.read_csv(str(ROOT_PATH)+"/data/stock_code.csv")
def data_insert(code:str,stock_data:pd.DataFrame):
    stock_data.reset_index(inplace=True)
    stock_data['Date'] = stock_data['Date'].dt.strftime('%Y-%m-%d')
    print("data columns:{}".format(stock_data.columns))

    #将数据写入到数据库中
    stock_data["id"] = [uuid.uuid4().hex for _ in range(len(stock_data))]
    stock_data["code"] = code
    stock_data["status"] = 1
    stock_data.rename(columns={"Adj Close":"adj_close","Date":"date","Open":"open","Close":"close","High":"high","Low":"low","Volume":"volume"}, inplace=True)
    # 将DataFrame的第一行转换为对象
    stock_data_dict = stock_data.to_dict('records')
    print(stock_data_dict[:5])
    pydantic_items = [StocksModel(**item) for item in stock_data_dict]
    stocks_crud.add_stocks_to_db(pydantic_items)
    return True

def data_check_download(stock_code:str,end_date:str):
    # 数据检查,判断数据库中是否存在该数据，或存在的数据是否完整
    # 获取数据库中该只股票的最新一条数据
    result = stocks_crud.get_newest_stock_by_code(stock_code)
    if result is not None:
        db_stock_date = str(result.get("date"))
        #如果数据缺失，则下载缺失部分的数据
        if db_stock_date < end_date:
            logger.info(f"股票代码：{stock_code}的数据缺失，开始下载缺失部分数据")
            stock_data = download_stock_data(stock_code,db_stock_date,end_date)
            data_insert(stock_code,stock_data)
        else:
            logger.info(f"股票代码：{stock_code}的数据完整，无需下载")
    else:
        logger.info(f"股票代码：{stock_code}的数据不存在，开始下载全部数据")
        #数据库中没有该股票的数据，则下载全部数据
        stock_data = download_stock_all_data(stock_code)
        data_insert(stock_code, stock_data)

def data_search(code:str,start_date:str,end_date:str):
    logger.info("code:{},start_date:{},end_date:{}".format(code,start_date,end_date))
    #数据检查下载
    data_check_download(code,end_date)
    #数据查询
    stock_data = stocks_crud.search_stocks(code,start_date,end_date)
    chinese_name = stock_code_cn[stock_code_cn['Code'] == str(code) + ".US"]['产品名称'].values[0]
    logger.info("产品名称：{}".format(chinese_name))
    stock_data_ =[]
    for item in stock_data:
        item["chinese_name"] = chinese_name
        stock_data_.append(item)

    return stock_data_

def data_search_all(code:str):
    logger.info("code:{}".format(code))
    #数据查询
    stock_data = stocks_crud.search_stocks_all(code)
    chinese_name = stock_code_cn[stock_code_cn['Code'] == str(code) + ".US"]['产品名称'].values[0]
    logger.info("产品名称：{}".format(chinese_name))
    stock_data_ =[]
    for item in stock_data:
        item["chinese_name"] = chinese_name
        stock_data_.append(item)

    return stock_data_


if __name__ == '__main__':
    from pydantic import BaseModel
    #data_insert('000001','2023-01-01','2023-02-01')
    #df = data_insert('NIO','2023-01-01','2023-02-01')
    df = data_search('JD','2023-01-01','2023-02-01')
    print(df[:5])

