# 为flask_login功能提供支持的模块
# 该模块封装了userManage中的部分函数
# 该模块实现了flask用户登录中必要的功能


import pymysql
import uuid
from werkzeug.security import generate_password_hash
from flask_login import UserMixin  # 引入用户基类
from werkzeug.security import check_password_hash
from databaseCURD import getUserList
from userManage import createUser

db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')


def create_user(user_name, password):
    """创建一个用户"""
    return createUser(user_name, password)

def get_user(user_name):
    """根据用户名获得用户记录"""
    for user in getUserList():
        if user[0] == str(user_name):
            return {
                "name": user[0],
                "password": user[1],
                "id": user[2],
            }
    return None

def get_user_by_id(id):
    """根据用户ID获得用户记录"""
    for user in getUserList():
        if user[2] == int(id):
            return {
                "name": user[0],
                "password": user[1],
                "id": user[2],
            }
    return None

class User(UserMixin):
    """用户类"""
    def __init__(self, user):
        self.username = user.get("name")
        self.password_hash = user.get("password")
        self.id = user.get("id")

    def verify_password(self, password):
        """密码验证"""
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password) or self.password_hash == password

    def get_id(self):
        """获取用户ID"""
        return self.id

    @staticmethod
    def get(user_id):
        """根据用户ID获取用户实体，为 login_user 方法提供支持"""
        if not user_id:
            return None
        user = get_user_by_id(user_id)

        if user != None:
            return User(user)
        return None