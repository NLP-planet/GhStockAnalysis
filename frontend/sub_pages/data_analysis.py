import os
import pandas as pd
import requests
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st
from sub_pages import login
from collections import Counter
from streamlit_echarts import st_pyecharts
from streamlit_echarts import JsCode
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.globals import SymbolType
from pyecharts.commons.utils import JsCode
import streamlit.components.v1 as components
from constants.constants import DATA_SEARCH_ALL_URL


def data_analysis():
    st.write("""# 数据可视化分析""")
    st.sidebar.markdown('---')

    input_code = st.text_input("请输入股票代码:", key="stock_code")

    # 创建搜索按钮
    if st.button('搜索', key='search'):
        data_search_all(input_code)


def data_search_all(input_code):

    if input_code != "" :
        data = {"code": input_code}
        token = login.cookies.get("jwt-token", None)
        headers = {"Authorization": f'Bearer {token}'}
        response = requests.post(DATA_SEARCH_ALL_URL, headers=headers,json=data)
        if response.status_code == 401:
            st.warning("请先登录您的账户")
            return
        df =pd.DataFrame(response.json())
        df.drop_duplicates(subset=['date'], inplace=True)
        # 涨跌额 = 收盘价 - 开盘价；
        # 涨跌幅 =（涨跌额 / 开盘价）*100 %；
        df['涨跌额'] = list(map(lambda x, y: x - y, df['close'], df['open']))
        df['涨跌幅'] = list(map(lambda x, y: x / y, df['涨跌额'], df['open']))
        st.write('---')
        st.write("""## 数据集预览""")
        st.write('数据集: ' + str(df.shape[0]) + ' 行 ' + str(df.shape[1]) + '列.')
        st.dataframe(df)
        st.caption('数据来源: 来源于雅虎财经数据，数据下载后存储于本地的数据库中')
        #数据的基础分析
        show_describe(df)
        #数据各项指标的趋势图
        show_explore(df)

    else:
        st.error("请输入要查询的股票代码")
def show_describe(df:pd.DataFrame):
    #查看数据的基础信息
    st.write('---')
    st.markdown("## 数据统计分析")
    st.dataframe(df.describe())

def show_explore(df:pd.DataFrame):
    st.write('---')
    st.markdown("## 各个指标的趋势查看")
    #探索数据的开盘价、收盘价等信息
    analysis_list = ['open', 'close', 'adj_close', 'high', 'low','volume']
    colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'cyan']
    fig, axs = plt.subplots(3,2,figsize=(20,10))
    for idx, metric in enumerate(analysis_list, 0):
        i = int(idx/2)
        j = idx % 2

        axs[i, j].plot(df['date'], df[metric],color=colors[idx])
        axs[i, j].set_title(f"子图 ({metric})")
        axs[i, j].set_xlabel("Date")
        axs[i, j].set_ylabel(metric)

    # 使用 Streamlit 显示图表
    st.pyplot(fig)

