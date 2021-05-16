import pymysql

db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')

def userVerify(username, password):
    # cursor = db.cursor()
    # sql = "select password from users where"
    # cursor.execute(sql)
    # data = cursor.fetchall()
    # cursor.close()
    users = {'zlyang':'200128yzl', 'cjh':'cjhghs'}
    if username in users.keys() and users[username] == password:
        return True
    return False