import pymysql
import traceback

def create_table_bangumi(db, table_name):
    cursor=db.cursor()
    sql = "CREATE TABLE %s(\
            bangumi_id int not NULL,\
            title varchar(50) not NULL,\
            play_url varchar(50) not NULL,\
            episode varchar(50) not NULL,\
            last_update date not NULL,\
            PRIMARY KEY (bangumi_id),\
            foreign key (bangumi_id) references bangumi_list(bangumi_id)\
            on update cascade\
            on delete cascade)ENGINE=InnoDB DEFAULT CHARSET=utf8;"% \
            (table_name)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('create success !')
    except:
        print('create table %s error!'%(table_name))
        traceback.print_exc()

def create_table_cast(db):
    cursor=db.cursor()
    table_name="cast"
    sql="CREATE TABLE %s(\
        bangumi_id int not null,\
        character varchar(50),\
        actor varchar(50),\
        primary key (bangumi_id),\
        foreign key (bangumi_id) references bangumi_list(bangumi_id)\
        on update casecade\
        on delete casecade) ENGINE=InnoDB DEFAULT CHARSET=utf8;"% \
        (table_name)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('create success !')
    except:
        print('create table %s error!'%(table_name))
        traceback.print_exc()

def create_table_company(db):
    cursor=db.cursor()
    table_name="company"
    sql="create table %s\
        （\
        company_id int not null,\
        company_name varchar(50) not null,\
        masterpice vaechar(50),\
        primary key (company_id))ENGINE=InnoDB DEFAULT CHARSET=utf8;"% \
        (table_name)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('create success !')
    except:
        print('create table %s error!'%(table_name))
        traceback.print_exc()


def create_table_conduct(db):
    cursor=db.cursor()
    table_name="conduct"
    sql="create table %s\
        （\
        conduct_id int not null,\
        conduct_name varchar(50) not null,\
        masterpice vaechar(50),\
        primary key (conduct_id))ENGINE=InnoDB DEFAULT CHARSET=utf8;"% \
        (table_name)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('create success !')
    except:
        print('create table %s error!'%(table_name))
        traceback.print_exc()

#公司动漫关系
def create_table_bangumi_company(db):
    cursor=db.cursor()
    table_name="bangumi_company"
    sql="create table %s\
        （\
        bangumi_id int not null,\
        bangumi_name,\
        company_name varchar(50) not null,\
        primary key (bangumi_id),\
        foreign key (bangumi_id) reference bangumi_list(bangumi_id)\
        on update casecade\
        on delete casecade,\
        foreign key (company_name) reference company(company_name)\
        on update casecade\
        on delete casecade) ENGINE=InnoDB DEFAULT CHARSET=utf8;"%\
        (table_name)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('create success !')
    except:
        print('create table %s error!'%(table_name))
        traceback.print_exc()
    
#监督动漫关系
def create_table_bangumi_conduct(db):
    cursor=db.cursor()
    table_name="bangumi_conduct"
    sql="create table %s\
        （\
        bangumi_id int not null,\
        bangumi_name,\
        conduct_name varchar(50) not null,\
        primary key (bangumi_id),\
        foreign key (bangumi_id) reference bangumi_list(bangumi_id)\
        on update casecade\
        on delete casecade,\
        foreign key (conduct_name) reference conduct(conduct_name)\
        on update casecade\
        on delete casecade) ENGINE=InnoDB DEFAULT CHARSET=utf8;"%\
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



if __name__ == '__main__':
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    create_bangumi_table(db,'AGE')
    db.close()