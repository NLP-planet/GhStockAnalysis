'''
@Project ：PredictDemo 
@File    ：project_introduce.py
@IDE     ：PyCharm 
@Author  ：Gaogz
@Date    ：2024/10/15 17:21 
@Desc    ：
'''
import streamlit as st
from PIL import Image

def create_introduce():
    st.sidebar.markdown('---')
    st.sidebar.image(Image.open('frontend/images/gh_001.jpg'))

    st.markdown("""
    # 关于股票的预测分析
    #### 项目地址: [github](https://github.com/NLP-planet/GhStockAnalysis)
    """)

    st.image(Image.open('frontend/images/gh_002.jpg'), caption='')
    st.markdown('---')

    st.markdown("""
                # 1. 项目背景
    
                随着社会的发展和人民生活水平的提高，越来越多的人开始将闲余的资金投入股市，进行金融理财。
    
                *本项目将对股票数据进行数据分析，窥探数据的秘密，随后使用机器学习模型对股价进行预测、对用户的问题实现基本理解完成数据问答*
                
                **⚠️警告:投资有风险，入市需谨慎！！**
    """)
    st.markdown("""
    
                # 2. 项目分工
    
                #### 任务列表：
                1. 编写爬虫程序，数据爬取
                2. 进行数据清洗和特征工程
                3. Adaboost模型搭建与调参
                4. 利用pyechart对数据集可视化分析
                5. 探索性数据分析
                6. 机器学习模型搭建(Random Forest, GBDT, XGBoost, LIghtGBM)
                7. 模型评估
                8. web应用制作
    
                # 3. 相关技术
                ### 3.1 框架
                采用前后端分离,后台服务采用fastapiweb框架,前端页面采用streamlit搭建
    
                ### 3.1数据获取
    
                使用yfinance完成对雅虎财经个别股票数据的下载,下载后将数据存储于本地的sqlite数据库中。
    
                ### 3.2可视化
    
                可视化的过程中，我们使用了python强大的可视化神器——pyechart, 使用它可以绘制出一些好看的图，让数据的呈现更加直观
    
    
                ### 3.3运用模型
    
                ###### 3.3.1 随机森林
    
                利用多棵树对样本进行训练并预测的一种分类器
    
                ###### 3.3.2 GBDT
    
                由多棵决策树组成,所有树的结论累加起来做最终答案
    
                ###### 3.3.3 XGBoost
    
                XGBoost高效地实现了GBDT算法并进行了算法和工程上的许多改进
    
                ###### 3.3.4 LightGBM
    
                LightGBM是在GBDT算法框架下的一种改进实现，是一种基于决策树算法的快速、分布式、高性能的GBDT框架
    
                # 4.结论
    
    """)

