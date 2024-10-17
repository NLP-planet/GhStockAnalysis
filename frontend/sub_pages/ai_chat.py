'''
@Project ：GhStockAnalysis 
@File    ：ai_chat.py
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
from streamlit_chat import message
from streamlit.components.v1 import html
from sub_pages import login
from constants.constants import CHAT_URL



def init_chat():
    # audio_path = "https://docs.google.com/uc?export=open&id=16QSvoLWNxeqco_Wb2JvzaReSAw5ow6Cl"
    # img_path = "https://www.groundzeroweb.com/wp-content/uploads/2017/05/Funny-Cat-Memes-11.jpg"
    # youtube_embed = '''
    # <iframe width="400" height="215" src="https://www.youtube.com/embed/LMQ5Gauy17k" title="YouTube video player" frameborder="0" allow="accelerometer; encrypted-media;"></iframe>
    # '''
    #
    # markdown = """
    # ### HTML in markdown is ~quite~ **unsafe**
    # <blockquote>
    #   However, if you are in a trusted environment (you trust the markdown). You can use allow_html props to enable support for html.
    # </blockquote>
    #
    # * Lists
    # * [ ] todo
    # * [x] done
    #
    # Math:
    #
    # Lift($L$) can be determined by Lift Coefficient ($C_L$) like the following
    # equation.
    #
    # $$
    # L = \\frac{1}{2} \\rho v^2 S C_L
    # $$
    #
    # ~~~py
    # import streamlit as st
    #
    # st.write("Python code block")
    # ~~~
    #
    # ~~~js
    # console.log("Here is some JavaScript code")
    # ~~~
    #
    # """
    #
    # table_markdown = '''
    # A Table:
    #
    # | Feature     | Support              |
    # | ----------: | :------------------- |
    # | CommonMark  | 100%                 |
    # | GFM         | 100% w/ `remark-gfm` |
    # '''
    #
    # st.session_state.setdefault(
    #     'past',
    #     ['plan text with line break',
    #      'play the song "Dancing Vegetables"',
    #      'show me image of cat',
    #      'and video of it',
    #      'show me some markdown sample',
    #      'table in markdown']
    # )
    # chart_data = pd.DataFrame(
    # np.random.randn(20, 3),
    # columns=['a', 'b', 'c'])
    # st.session_state.setdefault(
    #     'generated',
    #     [{'type': 'normal', 'data': 'Line 1 \n Line 2 \n Line 3'},
    #      {'type': 'normal', 'data': f'<audio controls src="{audio_path}"></audio>'},
    #      {'type': 'normal', 'data': f'<img width="100%" height="200" src="{img_path}"/>'},
    #      {'type': 'normal', 'data': f'{youtube_embed}'},
    #      {'type': 'normal', 'data': f'{markdown}'},
    #      {'type': 'table', 'data': f'{table_markdown}'}]
    #
    # )

    st.title("智慧问答")
    message("你好，我是您的机器人环环，我可以为您提供查数服务！")

    chat_placeholder = st.empty()
    with chat_placeholder.container():
        if "chat_history" in st.session_state.keys():
            user_idx = 0
            for msg in st.session_state['chat_history']:
                if msg.get("is_user"):
                    message(msg.get("data"), is_user=True, key=f"{user_idx}_user")
                    user_idx+=1
                else:
                    if isinstance(msg.get("data"),dict):
                        #图表
                        chart_type = msg.get("data").get("chart_type")
                        data_df = msg.get("data").get("data")
                        logger.info(f"图表类型{chart_type}")
                        if chart_type != "table":
                            data_df = data_df.drop(['chinese_name', 'code','date'], axis=1)

                        if chart_type == "line":
                            st.line_chart(data_df)
                        elif chart_type == "pie":
                            pass
                        elif chart_type == "bar":
                            st.bar_chart(data_df)
                        else:
                            st.table(msg.get("data").get("data"))

                    else:
                        message(
                            msg.get("data"),
                            key=f"{user_idx}",
                            allow_html=True)


        st.button("清空会话", on_click=on_btn_click)

    with st.container():
        st.text_input("请输入您的问题:", on_change=on_input_change, key="user_input")

def on_input_change():
    user_input = st.session_state.user_input

    if "chat_history" not in st.session_state.keys():
        st.session_state.setdefault("chat_history", [{"is_user": True, "data": user_input}])
    else:
        st.session_state.chat_history.append({"is_user": True, "data": user_input})

    if user_input != "":
        data = {"user_input": user_input}
        token = login.cookies.get("jwt-token", None)
        headers = {"Authorization": f'Bearer {token}'}
        response = requests.post(CHAT_URL, headers=headers,json=data)
        if response.status_code == 401:
            st.warning("请先登录您的账户")
            return
        resp_data= response.json()
        if resp_data is not None:
            df =pd.DataFrame(resp_data.get('data',[]))
            df.drop_duplicates(subset=['date'], inplace=True)
            st.session_state.chat_history.append({"is_user": False, "data":"您要查询的数据如下"})
            st.session_state.chat_history.append({"is_user": False, "data": {"chart_type":resp_data.get('chart_type','table'),"data":df}})
    else:
        st.error("请输入要查询的内容")

def on_btn_click():
    del st.session_state.chat_history[:]




