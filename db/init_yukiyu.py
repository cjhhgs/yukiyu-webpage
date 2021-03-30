import pymysql

def init_db_yukiyu():
    name = "yukiyu"

    db = pymysql.connect(host='127.0.0.1', port=3306, user='jhchen', password='123456',charset='utf8')

    cursor = db.cursor()

    sql = "create database if not exists yukiyu"

    cursor.execute(sql)
    db.close()

def init_table_bilibili():
    db = pymysql.connect(host='127.0.0.1', port=3306, user='jhchen', password='123456',charset='utf8', database="yukiyu")
    cursor = db.cursor()

    sql1 = "drop table if exists bilibili"
    sql2 = """create table bilibili (
        bangumi_id int NOT NULL,
        title varchar(50) NOT NULL,
        play_url varchar(150) NOT NULL,
        episode varchar(10) NOT NULL,
        last_update date NOT NULL,
        primary key(bangumi_id)
        )"""

    cursor.execute(sql1)
    cursor.execute(sql2)
    db.close()

def init_table_bangumi():
    db = pymysql.connect(host='127.0.0.1', port=3306, user='jhchen', password='123456',charset='utf8', database="yukiyu")
    cursor = db.cursor()

    sql1 = "drop table if exists bangumi_list"
    sql2 = """create table bangumi_list (
        bangumi_id int NOT NULL,
        name varchar(80) NOT NULL,
        img varchar(100) NOT NULL,
        primary key(bangumi_id)
        )"""

    cursor.execute(sql1)
    cursor.execute(sql2)
    db.close()

if __name__ == '__main__':
    init_db_yukiyu()
    init_table_bangumi()
    init_table_bilibili()