'''
@Project ：GhStockAnalysis 
@File    ：stocks_crud.py
@IDE     ：PyCharm 
@Author  ：Gaogz
@Date    ：2024/10/16 10:15 
@Desc    ：
'''
import uuid
from typing import Dict,List

from database.models.models import StocksModel
from sqlalchemy import and_
from database.session import with_session


@with_session
def add_stocks_to_db(
    session,
    stocks:List[StocksModel]):
    """
    批量插入股票数据
    """
    session.bulk_save_objects(stocks)
    session.commit()
    return "Data inserted successfully."

@with_session
def add_one_stock_to_db(
    session,
    stock:StocksModel):
    """
    批量插入股票数据
    """
    session.add(stock)
    session.commit()
    return "Data inserted successfully."

@with_session
def get_newest_stock_by_code(session, stock_code) -> StocksModel:
    """
    查询股票数据，通过股票码
    """
    m = (session.query(StocksModel).filter(and_(StocksModel.code==stock_code,StocksModel.status==1))
         .order_by(StocksModel.date.desc())
         .first())
    if m is not None:
        return {"open": m.open, "close": m.close, "high": m.high, "low": m.low, "date": m.date}
    return m
@with_session
def search_stocks(session, stock_code: str, start_date: str,end_date:str):
    Stocks = (
        session.query(StocksModel)
        .filter_by(code=stock_code)
        .filter(StocksModel.date >=start_date)
        .filter(StocksModel.date <=end_date)
        .order_by(StocksModel.date)
        .all()
    )
    # 直接返回 List[StocksModel] 报错
    data = []
    for m in Stocks:
        data.append({"code":m.code,"date": m.date,"open": m.open, "close": m.close,"adj_close":m.adj_close, "high": m.high, "low": m.low,"volume": m.volume })
    return data

@with_session
def search_stocks_all(session, stock_code: str):
    Stocks = (
        session.query(StocksModel)
        .filter_by(code=stock_code)
        .order_by(StocksModel.date)
        .all()
    )
    # 直接返回 List[StocksModel] 报错
    data = []
    for m in Stocks:
        data.append({"code":m.code,"date": m.date,"open": m.open, "close": m.close,"adj_close":m.adj_close, "high": m.high, "low": m.low,"volume": m.volume })
    return data

@with_session
def del_stocks(session, stock_code: str):
    stocks = (
        session.query(StocksModel)
        .filter_by(code=stock_code)
        .filter(StocksModel.status==1)
        .all()
    )
    for m in stocks:
        m.status=2
        session.add(m)
    session.commit()