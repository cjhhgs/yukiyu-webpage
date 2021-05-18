#此页为存储过程

import pymysql
import traceback

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


#user存储过程
def createStoreProcedureUser(db):
    cursor= db.cursor()
    sql="""
        delimiter $$
        drop procedure if exists insert_user$$
        create procedure insert_user(
            in name varchar(20), 
            in password varchar(128), 
            in privilege char(4)
        )
        begin
            insert into user(name, password, privilege)
            values(name, password,privilege);
        end$$
        delimiter ;
    """


if __name__ == '__main__':
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="root", password="123456",charset='utf8')
    #存储过程，需要手动创建
    createStoreProcedureBConduct(db)
    createStoreProcedureBCompany(db)
    db.close()