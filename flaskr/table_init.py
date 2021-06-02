# 所有的表的初始化创建语句
# 可调用该模块进行表的初始化

import pymysql
import traceback
from viewAndTrigger_init import create_view_detail_info
from db_bangumi_insert import insert_bangumi
from dbBangumiInfoInsert import insert_bangumi_info

#bangumi_list总表
def create_table_bangumi_list(db):
    cursor=db.cursor()
    sql = """
        create table if not exists bangumi_list(
            bangumi_id int not null,
            name varchar(80) not null,
            img varchar(100) not null,
            primary key (bangumi_id))ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('create success !')
    except:
        print('create table bangumi_list error!')
        traceback.print_exc()


#动漫网站分表
def create_table_bangumi(db, table_name):
    cursor=db.cursor()
    sql = """CREATE TABLE if not exists %s(
            bangumi_id int not NULL,
            title varchar(50) not NULL,
            play_url varchar(50) not NULL,
            episode varchar(50) not NULL,
            last_update date not NULL,
            PRIMARY KEY (bangumi_id),
            foreign key (bangumi_id) references bangumi_list(bangumi_id)
            on update cascade
            on delete cascade)ENGINE=InnoDB DEFAULT CHARSET=utf8;"""% \
            (table_name)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('create success !')
    except:
        print('create table %s error!'%(table_name))
        traceback.print_exc()

#声优表
def create_table_cast(db):
    cursor=db.cursor()
    table_name="bangumi_cast"
    sql="""CREATE TABLE if not exists %s(
        bangumi_id int not null,
        actor varchar(50) not null,
        primary key (bangumi_id, actor),
        foreign key (bangumi_id) references bangumi_list(bangumi_id)
        on update cascade
        on delete cascade) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""% \
        (table_name)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('create success !')
    except:
        print('create table %s error!'%(table_name))
        traceback.print_exc()

#制作公司表
def create_table_company(db):
    cursor=db.cursor()
    table_name="company"
    sql="""
        create table %s(
        company_id int primary key auto_increment,
        company_name varchar(50) not null,
        masterpiece varchar(50)) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""% \
        (table_name)
    sql2="""drop table if exists bangumi_company;"""
    sql3="drop table if exists %s;"%(table_name)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql2)
        cursor.execute(sql3)
        cursor.execute(sql)
        print('create success !')
    except:
        print('create table %s error!'%(table_name))
        traceback.print_exc()


# 监督表
def create_table_conduct(db):
    cursor=db.cursor()
    table_name="conduct"
    sql1="drop table if exists bangumi_conduct;"
    sql2="drop table if exists conduct;"
    sql3="""create table if not exists conduct(
        conduct_id int primary key auto_increment,
        conduct_name varchar(50) not null,
        masterpiece varchar(50))ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    try:
        print('start to execute:')
        print(sql3)
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        print('create success !')
    except:
        print('create table %s error!'%(table_name))
        traceback.print_exc()

#动漫-公司关系
def create_table_bangumi_company(db):
    cursor=db.cursor()
    table_name="bangumi_company"
    sql="""create table if not exists %s(
        bangumi_id int not null,
        company_id int not null,
        primary key (bangumi_id),
        foreign key (bangumi_id) references bangumi_list(bangumi_id)
        on update cascade
        on delete cascade,
        foreign key (company_id) references company(company_id)
        on update cascade
        on delete cascade) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""%\
        (table_name)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('create success !')
    except:
        print('create table %s error!'%(table_name))
        traceback.print_exc()
    
#动漫-监督关系
def create_table_bangumi_conduct(db):
    cursor=db.cursor()
    table_name="bangumi_conduct"
    sql="""create table if not exists %s(
        bangumi_id int not null,
        conduct_id int not null,
        primary key (bangumi_id),
        foreign key (bangumi_id) references bangumi_list(bangumi_id)
        on update cascade
        on delete cascade,
        foreign key (conduct_id) references conduct(conduct_id)
        on update cascade
        on delete cascade) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""% \
        (table_name)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('create success !')
    except:
        print('create table %s error!'%(table_name))
        traceback.print_exc()


#创用户表
def create_table_user(db):
    cursor=db.cursor()
    sql = """
        create table if not exists user_list(
            if_manager enum('Y','N') not null default 'N',
            user_id int auto_increment,
            name varchar(20) ,
            password varchar(128) not null,
            privilege char(4) not null default 'YNNN',
            primary key(user_id),
            unique key(name)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('create success !')
    except:
        print('create table error!')
        traceback.print_exc()
    


# 构造与制作相关的表
def initProduceTbale(db):
    create_table_conduct(db) 
    create_table_company(db)
    create_table_bangumi_company(db)
    create_table_bangumi_conduct(db)
    create_table_cast(db)

if __name__ == '__main__':
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    # create_table_bangumi_list(db)
    # create_table_bangumi(db,'bilibili')
    # create_table_bangumi(db,"acfun")
    # initProduceTbale(db)
    # create_table_user(db)
    # create_view_detail_info(db)
    insert_bangumi(db)
    insert_bangumi_info(db)
    db.close()
    