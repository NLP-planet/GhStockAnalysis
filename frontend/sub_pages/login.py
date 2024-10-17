import streamlit as st
import requests
from streamlit_cookies_manager import EncryptedCookieManager
from constants.constants import SIGNUP_URL,LOGIN_URL
import re

# This should be on top of your script
cookies = EncryptedCookieManager(
    # This prefix will get added to all your cookie names.
    # This way you can run your app on Streamlit Cloud without cookie name clashes with other apps.
    # prefix="ktosiek/streamlit-cookies-manager/",
    # You should really setup a long COOKIES_PASSWORD secret if you're running on Streamlit Cloud.
    password="ggz123456"
)
if not cookies.ready():
    # Wait for the component to load and send us current cookies.
    st.spinner()
    st.stop()

# Function for verifying valid email
def is_valid_email(email):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(email_pattern, email):
            return True
        else:
            return False

# Function for doing http request to backend for login
def login(username, password):
    data = {"username": username, "password": password}
    response = requests.post(LOGIN_URL, data=data)
    if response.status_code == 200:
        response_data = response.json()
        if "access_token" in response_data:
            access_token = response_data["access_token"]
            # Set the cookie (secure and with an appropriate expiration)
            cookies["jwt-token"] = access_token
            # "jwt-token" is cookie name
            cookies.save()
            return True
   
    return False

def signup(username, password):
    data = {"email": username, "password": password} # depend on the key (email, password)
    response = requests.post(SIGNUP_URL, json=data)
    if response.status_code == 201:
        return True
    if response.status_code == 409:
        return False

# Login and Sign Up page
def login_page():
    st.title("股票分析系统")
    choice = st.selectbox("登录/注册", ['登录', '注册'])
    if choice == '登录':
        email = st.text_input("邮箱地址")
        password = st.text_input("密码", type="password")
        if st.button("登录"):
            if login(email, password):
                st.success("登录成功!")
            else:
                st.error("账号或密码错误")
    
    if choice == '注册':
        email = st.text_input("邮箱地址")
        password = st.text_input("密码", type="password")
        confirm_password = st.text_input("确认密码", type="password")
        
        if st.button("注册"):
            if is_valid_email(email):
                if password != "" and confirm_password != "":
                    if password == confirm_password:
                        data = {"username": email, "password": password}
                        response = requests.post(SIGNUP_URL, json=data)
                        if signup(email, password):
                            st.success("注册成功!")
                        else:
                            st.error("该邮箱已经被注册")
                else:
                    st.error("请保持两次输入的密码一致！")
            else:
                st.error("你的邮箱号不正确")
            
