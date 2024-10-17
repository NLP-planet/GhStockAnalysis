'''
@Project ：GhStockAnalysis 
@File    ：constants.py
@IDE     ：PyCharm 
@Author  ：Gaogz
@Date    ：2024/10/16 16:41 
@Desc    ：
'''
BASE_URL = "http://127.0.0.1:9001/"
# URL backend for login
LOGIN_URL = BASE_URL+"users/login/"  # Change the url from your backend
SIGNUP_URL = BASE_URL+"users/register/"
DATA_SEARCH_URL = BASE_URL+"dataload/search/"
DATA_SEARCH_ALL_URL = BASE_URL+"dataload/all/"
CHAT_URL = BASE_URL+"chat/chat/"
