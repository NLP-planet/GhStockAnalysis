import streamlit as st
from streamlit_option_menu import option_menu
from sub_pages import login
from sub_pages import project_introduce
from sub_pages import data_analysis
from sub_pages import data_download
from sub_pages import ai_chat
from sub_pages import ai_predict
from sub_pages import data_process

with st.sidebar: # add this if you want to make sidebar
    st.markdown('<h2>项目菜单</h2>',
        unsafe_allow_html=True)
    selected = option_menu(
        menu_title="",
        options=["🏠Home", "📊数据查看","📊数据处理","📊数据分析","🙋‍智慧预测", "🙋‍智慧问答","🔐登录/注册"],
        icons=["🏠", "📊","📊","📰", "🩺", "🙋‍♂️", "🔐"],
       menu_icon="",
        default_index=0,
        orientation="vertical",
        styles={ 
            "nav-link": {"font-size": "18px", "text-align": "center", "margin":"0px", "white-space": "nowrap"}
        }
    )
    st.markdown("---")
    st.markdown(
        '<h6>Made in &nbsp&nbsp <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp&nbsp by &nbsp&nbsp&nbsp<a href="https://github.com/NLP-planet/GhStockAnalysis" style="font-family: 宋体; font-size:126%;">AIE51期-2</a></h6>',
        unsafe_allow_html=True
    )


if selected == "🏠Home":
    #首页放置关于项目的介绍
    project_introduce.create_introduce()

if selected == "📊数据查看":
    data_download.data_init()

if selected == "📊数据处理":
    data_process.init_process()
if selected =="📊数据分析":
    data_analysis.data_analysis()

if selected == "🙋‍智慧预测":
    ai_predict.predict_init()

if selected == "🙋‍智慧问答":
    ai_chat.init_chat()

if selected == "🔐登录/注册":
    login.login_page()



