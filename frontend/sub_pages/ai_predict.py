'''
@Project ：GhStockAnalysis 
@File    ：ai_predict.py
@IDE     ：PyCharm 
@Author  ：Gaogz
@Date    ：2024/10/16 09:16 
@Desc    ： 查考：https://github.com/chenwr727/stock-backtrader-web-app/blob/master/utils/processing.py
'''
import requests
import pandas as pd
import streamlit as st
from streamlit_echarts import st_pyecharts
from charts.stock import draw_pro_kline
from charts.results import draw_result_bar
from loguru import logger
from sub_pages import login
from constants.constants import DATA_SEARCH_URL

def predict_init():
    # 设置页面标题
    st.title('智慧预测')
    input_code = st.text_input("请输入股票代码:", key="stock_code")
    # 设定3列
    col1, col2, = st.columns(2)

    with col1:
        # 添加日期选择器
        start_date = st.date_input('开始日期:', value=None, key=None)
    with col2:
        end_date = st.date_input('结束日期:', value=None, key=None)

    # 创建搜索按钮
    if st.button('查看', key='search'):
        data_search(input_code, start_date, end_date)

    # st.subheader("Strategy")
    # name = st.selectbox("strategy", list(strategy.keys()))
    # submitted, params = params_selector_ui(strategy[name])
    # if submitted:
    #     logger.info(f"akshare: {ak_params}")
    #     logger.info(f"backtrader: {backtrader_params}")
    #     backtrader_params.update(
    #         {
    #             "stock_df": stock_df.iloc[:, :6],
    #             "strategy": StrategyBase(name=name, params=params),
    #         }
    #     )
    #     par_df = run_backtrader(**backtrader_params)
    #     st.dataframe(par_df.style.highlight_max(subset=par_df.columns[-3:]))
    #     bar = draw_result_bar(par_df)
    #     st_pyecharts(bar, height="500px")

def data_search(input_code, start_date, end_date):

    if start_date > end_date:
        st.error("开始时间不能大于结束时间")
        return

    print('开始时间：{},结束时间:{}'.format(start_date, end_date))
    if input_code != "" and start_date != None and end_date != None:
        data = {"code": input_code, "start_date": str(start_date),"end_date": str(end_date)}
        token = login.cookies.get("jwt-token", None)
        headers = {"Authorization": f'Bearer {token}'}
        response = requests.post(DATA_SEARCH_URL, headers=headers,json=data)
        if response.status_code == 401:
            st.warning("请先登录您的账户")
            return
        df =pd.DataFrame(response.json())
        df.drop_duplicates(subset=['date'], inplace=True)
        st.write('---')

        draw_kline(df)
    else:
        st.error("请输入要查询的股票代码和起止日期")
def draw_kline(df:pd.DataFrame):
    st.subheader("K线图")
    kline = draw_pro_kline(df)
    st_pyecharts(kline, height="500px")
    return kline