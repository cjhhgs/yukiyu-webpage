import pymysql
import traceback

def create_table_bangumi(db, table_name):
    cursor=db.cursor()
    sql = "CREATE TABLE if not exists %s(\
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

#声优表
def create_table_cast(db):
    cursor=db.cursor()
    table_name="bangumi_cast"
    sql="CREATE TABLE %s(\
        bangumi_id int not null,\
        actor varchar(50) not null,\
        primary key (bangumi_id, actor),\
        foreign key (bangumi_id) references bangumi_list(bangumi_id)\
        on update cascade\
        on delete cascade) ENGINE=InnoDB DEFAULT CHARSET=utf8;"% \
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

#bangumi_company存储过程
def createStoreProcedureBCompany(db):
    cursor=db.cursor()
    sql="""
        delimiter $$
        drop procedure if exists insertIntoCompany $$
        create procedure insertIntoCompany(
            in id int,
            in bangumi_name varchar(50),
            in new_company_name varchar(50))
        begin
            declare companyId int default 0;
            if new_company_name not in (select company_name from company) then
                begin
                insert into company(company_name,masterpiece)
                values 
                (new_company_name,bangumi_name);
                end;
            end if;
            if id not in (select bangumi_id from bangumi_company) then
                begin
                select company_id into companyId
                from company
                where company.company_name = new_company_name;
                insert into bangumi_company(bangumi_id, company_id)
                values
                (id, companyId);
                end;
            end if;

        end$$
        delimiter ;
        """
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('create success !')
    except:
        print('create error!')
        traceback.print_exc()


#bangumi_conduct存储过程
def createStoreProcedureBConduct(db):
    cursor=db.cursor()
    sql="""
        delimiter $$
        drop procedure if exists insertIntoConduct$$
        create procedure insertIntoConduct(in id int,in bangumi_name varchar(50),in new_conduct_name varchar(50))
        begin
            declare conductId int default 0;
            if (new_conduct_name not in (select conduct_name from conduct)) then
                begin
                
                insert into conduct(conduct_name,masterpiece)
                values 
                (new_conduct_name,bangumi_name);
                end;
            end if;
            if (id not in (select bangumi_id from bangumi_conduct)) then
                begin
                select conduct_id into conductId
                from conduct
                where conduct.conduct_name = new_conduct_name;
                insert into bangumi_conduct(bangumi_id, conduct_id)
                values
                (id, conductId);
                end;
            end if;
        end$$
        delimiter ;
        """
    try:

        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('create success !')
    except:
        print('error!')
        traceback.print_exc()

def testproc(db):
    cursor=db.cursor()
    name = "test"
    sql1 = """delimiter /"""
    sql2 = """drop procedure if exists %s/"""%\
        (name)
    sql3 = """
        create procedure test(in p1 int, in p2 varchar(50))
        begin
        end/"""
    sql4 = """delimiter ;"""
    try:
        print('start to execute:')
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        cursor.execute(sql4)
        print('create success !')
    except:
        print('error!')
        traceback.print_exc()

# 构造与制作相关的4个表
def initProduceTbale(db):
    # create_table_conduct(db) 
    # create_table_company(db)
    # create_table_bangumi_company(db)
    # create_table_bangumi_conduct(db)
    create_table_cast(db)

if __name__ == '__main__':
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    initProduceTbale(db)
    # createStoreProcedureBConduct(db)
    # createStoreProcedureBCompany(db)
    db.close()
    