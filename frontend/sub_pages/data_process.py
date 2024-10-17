'''
@Project ：GhStockAnalysis 
@File    ：data_process.py
@IDE     ：PyCharm 
@Author  ：Gaogz
@Date    ：2024/10/16 09:16 
@Desc    ：
'''
import numpy as np
import pandas as pd
from loguru import logger
import requests
import streamlit as st
from streamlit.components.v1 import html
from sub_pages import login
from constants.constants import CHAT_URL
import yfinance as yf
import matplotlib.pyplot as plt

def init_process():
    st.write("# 数据处理页面")


    # Streamlit 应用标题
    st.title("股票趋势图")

    # 输入股票代码
    ticker_symbol = st.text_input("输入股票代码（例如AAPL）:", "AAPL")

    # 获取股票历史数据
    def load_data(ticker):
        data = yf.download(ticker, start="2020-01-01", end="2024-01-01")
        data.reset_index(inplace=True)
        return data

    data_load_state = st.text("加载数据中...")
    data = load_data(ticker_symbol)
    data_load_state.text("加载数据完成!")

    # 绘制趋势图
    fig, ax = plt.subplots()

    # 绘制历史数据
    ax.plot(data["Date"], data["Close"], label="历史价格", color="blue")

    # 预测未来的简单线性延伸（这里仅做演示，实际预测可以用更复杂的算法）
    last_close_price = data["Close"].iloc[-1]
    future_dates = pd.date_range(data["Date"].iloc[-1], periods=30, freq="D")
    future_prices = last_close_price + np.linspace(0, 10, len(future_dates))

    # 绘制预测数据
    ax.plot(future_dates, future_prices, label="预测价格", color="red", linestyle="--")

    # 添加图例
    ax.legend()

    # 设置标题和标签
    ax.set_title(f"{ticker_symbol} 股票价格趋势")
    ax.set_xlabel("日期")
    ax.set_ylabel("价格 (USD)")

    # 使用 Streamlit 显示图表
    st.pyplot(fig)





