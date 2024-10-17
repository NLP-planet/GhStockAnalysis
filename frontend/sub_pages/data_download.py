'''
@Project ：PredictDemo 
@File    ：data_download.py
@IDE     ：PyCharm 
@Author  ：Gaogz
@Date    ：2024/10/15 22:46 
@Desc    ：
'''
import pandas as pd
import streamlit as st
import datetime
import requests
from streamlit_echarts import st_pyecharts
from streamlit_echarts import JsCode
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.globals import SymbolType
from pyecharts.commons.utils import JsCode
from sub_pages import login
from constants.constants import DATA_SEARCH_URL

def data_init():
    # 设置页面标题
    st.title('数据查看')
    input_code = st.text_input("请输入股票代码:", key="stock_code")
    #设定3列
    col1, col2,= st.columns(2)

    with col1:
        # 添加日期选择器
        start_date = st.date_input('开始日期:', value=None, key=None)
    with col2:
        end_date = st.date_input('结束日期:', value=None, key=None)

    # 创建搜索按钮
    if st.button('搜索', key='search'):
        data_search(input_code,start_date,end_date)

    # # 创建下载按钮
    # if st.button('下载', key='download'):
    #     data_download(input_code, start_date, end_date)
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
        # 涨跌额 = 收盘价 - 开盘价；
        # 涨跌幅 =（涨跌额 / 开盘价）*100 %；
        df['涨跌额'] = list(map(lambda x, y: x - y, df['close'], df['open']))
        df['涨跌幅'] = list(map(lambda x, y: x / y, df['涨跌额'], df['open']))

        st.write("""## 数据集预览""")
        st.write('数据集: ' + str(df.shape[0]) + ' 行 ' + str(df.shape[1]) + '列.')
        st.dataframe(df)
        st.caption('数据来源: 来源于雅虎财经数据，数据下载后存储于本地的数据库中')
        data_basic_analysis(df.tail(15))


    else:
        st.error("请输入要查询的股票代码和起止日期")


def data_basic_analysis(top_df):
    st.write('---')
    st.write("""##### 近十五天涨跌额-成交量趋势图""")

    bar = Line(init_opts=opts.InitOpts(theme='dark',
                                      width='1000px',
                                      height='600px', )
              )
    bar.add_xaxis(top_df['date'].tolist())
    # 添加一个Y轴
    bar.extend_axis(yaxis=opts.AxisOpts(type_="value",
                                        position="right",
                                        is_scale=True,
                                        axislabel_opts=opts.LabelOpts(margin=20, color="#74673E",
                                                                      formatter=
                                                                      JsCode(
                                                                          """function (value)
                                                                          {return Math.floor(value);}""")),
                                        axisline_opts=opts.AxisLineOpts(
                                            linestyle_opts=opts.LineStyleOpts(
                                                width=2, color="#B5CAA0")
                                        ),
                                        axistick_opts=opts.AxisTickOpts(
                                            is_show=True,
                                            length=15,
                                            linestyle_opts=opts.LineStyleOpts(
                                                color="#D9CD90")
                                        ),
                                        ))
    bar.add_yaxis('成交量', top_df['volume'].tolist(), yaxis_index=0,
                  is_smooth=True,
                  symbol_size=8,
                  color='red',
                  z_level=1,
                  itemstyle_opts=opts.ItemStyleOpts(color='#00AA90'),
                  label_opts=opts.LabelOpts(is_show=False),
                  linestyle_opts={
                      'normal': {
                          'width': 3,
                          'shadowColor': 'rgba(0, 0, 0, 0.5)',
                          'shadowBlur': 5,
                          'shadowOffsetY': 10,
                          'shadowOffsetX': 10,
                          'curve': 0.5,
                          'color': '#00AA10'
                      }
                  }
                  )
    bar.set_global_opts(
        # visualmap_opts=opts.VisualMapOpts(type_='color', min_=500, max_=2000,series_index=0,
        #                                   range_color=['#0071ce', '#ffc220', '#ffffff']),
        title_opts=opts.TitleOpts(title="",
                                  pos_left="center",
                                  pos_top='1%',
                                  title_textstyle_opts=opts.TextStyleOpts(
                                      font_size=20,
                                      color='#00BFFF')),
        legend_opts=opts.LegendOpts(is_show=True, pos_top='6%'),
        xaxis_opts=opts.AxisOpts(boundary_gap=False,
                                 is_show=False,
                                 axislabel_opts=opts.LabelOpts(
                                     margin=30, color="#74673E"),
                                 axisline_opts=opts.AxisLineOpts(
                                     is_show=False),
                                 axistick_opts=opts.AxisTickOpts(
                                     is_show=True,
                                     length=10,
                                     linestyle_opts=opts.LineStyleOpts(
                                         color="#D9CD90"),
                                 ),
                                 splitline_opts=opts.SplitLineOpts(
                                     is_show=True, linestyle_opts=opts.LineStyleOpts(
                                         color="#D9CD90")
                                 ),
                                 ),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            position="left",
            is_scale=True,
            axislabel_opts=opts.LabelOpts(margin=20,
                                          color="#74673E",
                                          formatter=JsCode(
                                              """function (value) {return Math.floor(value);}""")),
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(
                    width=2, color="#B5CAA0")
            ),
            axistick_opts=opts.AxisTickOpts(
                is_show=True,
                length=15,
                linestyle_opts=opts.LineStyleOpts(
                    color="#D9CD90"),
            ),
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(
                    color="#D9CD90")
            ),
        )
    )

    line = Line(init_opts=opts.InitOpts(theme='light',
                                        width='1000px',
                                        height='600px'))
    line.add_xaxis(top_df['date'].tolist(),
                   )
    # 将line数据通过yaxis_index指向后添加的Y轴
    line.add_yaxis('涨跌额', top_df['涨跌额'].tolist(), yaxis_index=1,
                   is_smooth=True,
                   symbol_size=8,
                   color='red',
                   z_level=1,
                   label_opts=opts.LabelOpts(is_show=False),
                   itemstyle_opts=opts.ItemStyleOpts(color='#563F2E'),
                   linestyle_opts={
                       'normal': {
                           'width': 3,
                           'shadowColor': 'rgba(0, 0, 0, 0.5)',
                           'shadowBlur': 5,
                           'shadowOffsetY': 10,
                           'shadowOffsetX': 10,
                           'curve': 0.5,
                           'color': '#E16B8C'
                       }
                   })

    bar.overlap(line)
    st_pyecharts(bar, width=1000, height=600)

    st.write("""
        #####  结论
        基本上成交量和涨跌额呈反比，体现出股民们追涨止跌的心态(股价上涨，则持续持有该股票，股价下跌，则快速抛售股票！)
        """)
