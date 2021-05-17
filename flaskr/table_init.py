import pymysql
import traceback

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
    sql="""CREATE TABLE %s(
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
    

# def create_view_bangumi_cast(db):
#     cursor=db.cursor()
#     view_name = "bangumi_cast"
#     sql="CREATE view %s\
#         (bangumi_id, name, episode, company)
#         "

# 构造与制作相关的4个表
def initProduceTbale(db):
    create_table_conduct(db) 
    create_table_company(db)
    create_table_bangumi_company(db)
    create_table_bangumi_conduct(db)
    create_table_cast(db)

if __name__ == '__main__':
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    create_table_bangumi_list(db)
    create_table_bangumi(db,'bilibili')
    create_table_bangumi(db,"acfun")
    create_table_bangumi(db,"AGE")
    initProduceTbale(db)
    db.close()
    