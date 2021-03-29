import pymysql

def drop_db_yukiyu():

    db = pymysql.connect(host='127.0.0.1', port=3306, user='jhchen', password='123456',charset='utf8')

    cursor = db.cursor()

    sql = "drop database yukiyu"

    cursor.execute(sql)
    db.close()

if __name__=='__main__':
    drop_db_yukiyu()