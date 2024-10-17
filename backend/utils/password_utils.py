'''
@Project ：PredictDemo 
@File    ：password_utils.py
@IDE     ：PyCharm 
@Author  ：Gaogz
@Date    ：2024/10/15 14:55 
@Desc    ：
'''
from passlib.context import CryptContext # In this case it used for hashing the password

# 创建 CryptContext 对象，指定哈希算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto') # password hashing using bcrypt algorithm

def hash_pwd(password: str):
    return pwd_context.hash(password)

def verify_pwd(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 示例使用
if __name__ == "__main__":
    # 输入密码
    password = "mysecretpassword"

    # 加密密码
    hashed_password = hash_pwd(password)
    print(f"加密后的密码: {hashed_password}")

    # 验证密码是否正确
    is_valid = verify_pwd("mysecretpassword", hashed_password)
    print(f"密码验证结果: {is_valid}")





