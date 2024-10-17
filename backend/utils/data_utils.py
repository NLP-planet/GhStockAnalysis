'''
@Project ：PredictDemo 
@File    ：data_download.py
@IDE     ：PyCharm 
@Author  ：Gaogz
@Date    ：2024/10/15 21:24 
@Desc    ：
'''
import pandas as pd
import os
import json
import requests
import time
import glob
from loguru import logger
import yfinance as yf
import datetime as dt

# ----------------------下载某只股票数据------------------- #
# code:股票编码 日期格式：2019-05-21 filename：写到要存放数据的根目录
# length是筛选股票长度，默认值为False，既不做筛选，可人为指定长度，如200，既少于200天的股票不保存


def download_stock_data(ticker, start_date, end_date):
    """
    下载指定股票代码指定日期的数据
    period‌：指定要下载的数据周期，如“1d”、“5d”、“1mo”等。
    interval‌：指定数据间隔，如“1m”、“2m”、“1h”等。
    start 和 end‌：指定数据的开始和结束日期。
    threads‌：指定下载数据时使用的线程数。
    proxy‌：指定代理服务器的地址和端口，用于在中国大陆使用yfinance时绕过地域限制‌13。
    :param ticker: 股票代码
    :param start_date: 开始时间
    :param end_date:  截止时间
    :return:
    """
    # 下载指定股票的历史数据
    #yf.download(tickers, start=None, end=None, period='900d', interval='1d', actions=False, threads=True)
    stock_data = yf.download(tickers=ticker, start=start_date, end=end_date,)
    # date：日期；
    # Open：开盘价；
    # High：最高价；
    # Low：最低价；
    # Close: 收盘价；
    # Adj Close：调整收盘价；
    # Volume：交易量。
    logger.info(stock_data.head())  # 打印前几行数据查看
    logger.info(f'股票代码：{ticker} 共有%s天数据' % len(stock_data))
    # filename=ticker.replace('.', '_')
    # if len(stock_data) >0:
    #     stock_data.to_csv(os.path.join(ROOT_PATH,"data",filename+".csv"))
    #     logger.info(f"Data has been saved to {filename}.csv")
    # else:
    #     logger.warning(f"Not find data about {ticker}.")

    return stock_data

def download_stock_all_data(ticker:str):
    """
    下载指定股票代码上市以来的所有数据
    :param ticker:
    :return:
    """
    stock_data = yf.download(ticker, period="max")  # 下载该股票自上市以来的所有数据
    logger.info(stock_data.head())  # 打印前几行数据查看
    logger.info(f'股票代码：{ticker} 共有%s天数据' % len(stock_data))
    return stock_data

if __name__ == '__main__':
    # 比亚迪A股的股票代码
    ticker = "002594.SZ"
    # 蔚来
    ticker = "NIO"
    # 定义开始日期和结束日期
    end_date = dt.datetime.now()
    start_date = end_date - dt.timedelta(days=5 * 365)  # 回溯五年
    # 下载数据
    stock_data = download_stock_data(ticker, start_date, end_date)
    file_name = ticker.replace('.', '_')




