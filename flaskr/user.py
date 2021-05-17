import pymysql
import uuid
from werkzeug.security import generate_password_hash
from flask_login import UserMixin  # 引入用户基类
from werkzeug.security import check_password_hash

db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
users = [
    {
        'name': 'zlyang',
        'password': generate_password_hash('200128yzl')
    },
    {
        'name':'cjh',
        'password': generate_password_hash('cjhghs')
    }
]

def create_user(user_name, password):
    """创建一个用户"""
    user = {
        "name": user_name,
        "password": generate_password_hash(password),
        "id": uuid.uuid4()
    }
    users.append(user)

def get_user(user_name):
    """根据用户名获得用户记录"""
    for user in users:
        if user.get("name") == user_name:
            return user
    return None

def userVerify(username, password):
    # cursor = db.cursor()
    # sql = "select password from users where"
    # cursor.execute(sql)
    # data = cursor.fetchall()
    # cursor.close()
    
    if username in users.keys() and users[username] == password:
        return True
    return False

class User(UserMixin):
    """用户类"""
    def __init__(self, user):
        self.username = user.get("name")
        self.password_hash = user.get("password")
        self.id = user.get("name")

    def verify_password(self, password):
        """密码验证"""
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """获取用户ID"""
        return self.id

    @staticmethod
    def get(user_id):
        """根据用户ID获取用户实体，为 login_user 方法提供支持"""
        if not user_id:
            return None
        for user in users:
            if user.get('id') == user_id:
                return User(user)
        return None